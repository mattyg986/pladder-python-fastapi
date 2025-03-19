import logging
import os
import datetime
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
import pathlib
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.supabase_client import supabase, get_supabase
from app.api import api_router
from agents import set_tracing_disabled, enable_verbose_stdout_logging, set_default_openai_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Purple Ladder AI Agents Platform API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth check helper function
async def is_authenticated(request: Request) -> bool:
    """Check if the request has a valid auth token."""
    # First try Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
    else:
        # Try to get token from cookies
        sb_auth_token = request.cookies.get("sb-access-token")
        if not sb_auth_token:
            return False
        token = sb_auth_token
    
    try:
        # Verify with Supabase
        supabase = get_supabase()
        response = supabase.auth.get_user(token)
        return response.user is not None
    except Exception as e:
        logger.debug(f"Auth check failed: {str(e)}")
        return False

# Import API routers - must be before the static file handlers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Add health check endpoint
@app.get("/api/health")
def health_check():
    """Health check endpoint that returns JSON."""
    return {"status": "healthy", "timestamp": str(datetime.datetime.now())}

# Check if we're in a production environment
is_production = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PRODUCTION")

# Define public paths that don't require authentication
PUBLIC_PATHS = {
    "/",  # Add root path as public
    "/signin",
    "/static",
    "/api/health",
    "/favicon.ico",
    "/manifest.json",
    "/logo192.png",
    "/logo512.png",
    "/api/docs",
    "/api/openapi.json"
}

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Middleware to check authentication for all routes except public ones."""
    path = request.url.path
    
    # Skip auth check for public paths and static files
    if any(path.startswith(public_path) for public_path in PUBLIC_PATHS):
        # If authenticated user tries to access signin, redirect to dashboard
        if path == "/signin":
            is_auth = await is_authenticated(request)
            if is_auth:
                return RedirectResponse(url="/dashboard", status_code=302)
        response = await call_next(request)
        return response
    
    # Skip auth check for API routes (they handle their own auth)
    if path.startswith("/api/"):
        response = await call_next(request)
        return response
    
    # Check authentication
    is_auth = await is_authenticated(request)
    
    # For all other routes, require authentication
    if not is_auth:
        return RedirectResponse(url="/signin", status_code=302)
    
    response = await call_next(request)
    return response

# Handle production static files (built React app)
static_dir = pathlib.Path(__file__).parent / "static"
if is_production and static_dir.exists():
    logger.info(f"Serving static files from {static_dir}")
    
    # First mount specific static files at root level
    for static_file in ["favicon.ico", "manifest.json", "logo192.png", "logo512.png"]:
        file_path = static_dir / static_file
        if file_path.exists():
            app.mount(f"/{static_file}", StaticFiles(directory=str(static_dir), html=True, check_dir=False), name=static_file)
    
    # Then mount the static directory for JS/CSS assets
    static_assets_dir = static_dir / "static"
    if static_assets_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_assets_dir)), name="static")

# Serve index.html for all non-file routes in production
@app.get("/{catch_all:path}")
async def serve_frontend(catch_all: str, request: Request):
    """Serve frontend for all other routes in production."""
    if not is_production or not static_dir.exists():
        return JSONResponse({"detail": "Not found"}, status_code=404)
    
    # For authenticated users trying to access signin, redirect to dashboard
    is_auth = await is_authenticated(request)
    if is_auth and catch_all == "signin":
        return RedirectResponse(url="/dashboard", status_code=302)
    
    # For unauthenticated users, only allow public paths
    if not is_auth and catch_all not in ["", "signin"]:
        return RedirectResponse(url="/signin", status_code=302)
    
    # For all routes, serve index.html
    index_path = static_dir / "index.html"
    if index_path.exists():
        response = FileResponse(index_path)
        response.headers["Cache-Control"] = "no-store, max-age=0"
        return response
    
    return JSONResponse({"detail": "Not found"}, status_code=404)

@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    try:
        # Initialize Supabase connection
        logger.info("Checking Supabase connection...")
        sb = get_supabase()
        if sb:
            # Check connection to Supabase
            user_count = sb.table('agents').select('id').execute()
            logger.info(f"Supabase connection successful")
            
            # Initialize sample data if needed
            logger.info("Checking for existing agents in Supabase...")
            agents_data = sb.table('agents').select('*').execute()
            if not agents_data.data:
                logger.info("No agents found. Creating sample agents...")
                # Create sample agents in Supabase
                sample_agents = [
                    {
                        "name": "Recruiter Agent",
                        "type": "recruiter",
                        "description": "AI agent for candidate sourcing and evaluation",
                        "status": "active",
                        "parameters": {
                            "matching_threshold": 0.7,
                            "max_candidates": 10
                        }
                    },
                    {
                        "name": "Application Processor",
                        "type": "processor",
                        "description": "AI agent for processing job applications",
                        "status": "active",
                        "parameters": {
                            "auto_reject_threshold": 0.3,
                            "auto_advance_threshold": 0.8
                        }
                    },
                    {
                        "name": "Job Matcher",
                        "type": "matcher",
                        "description": "AI agent for matching candidates to jobs",
                        "status": "active",
                        "parameters": {
                            "similarity_algorithm": "cosine",
                            "minimum_score": 0.6
                        }
                    }
                ]
                
                for agent in sample_agents:
                    sb.table('agents').insert(agent).execute()
                
                logger.info(f"Created {len(sample_agents)} sample agents")
            else:
                logger.info(f"Found {len(agents_data.data)} existing agents in Supabase")
            
        logger.info("Supabase initialization complete.")
    except Exception as e:
        logger.error(f"Error initializing Supabase: {str(e)}")
        logger.warning("Continuing startup despite Supabase error.")
    
    # Initialize Agents SDK
    try:
        logger.info("Setting up OpenAI Agents SDK...")
        # Configure agents SDK only if API key is set
        if os.getenv("OPENAI_API_KEY"):
            # Set API key
            set_default_openai_key(os.getenv("OPENAI_API_KEY"))
            # Enable tracing
            set_tracing_disabled(False)
            # Enable verbose logging for development
            if not is_production:
                enable_verbose_stdout_logging()
            logger.info("Agents SDK initialized successfully")
        else:
            logger.warning("OPENAI_API_KEY not set, Agents SDK may not work correctly")
    except Exception as e:
        logger.error(f"Error setting up Agents SDK: {str(e)}")
        logger.warning("Continuing startup despite Agents SDK error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=not is_production
    ) 