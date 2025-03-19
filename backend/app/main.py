import logging
import os
import datetime
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
import pathlib
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.supabase_client import get_supabase
from app.core.auth import get_token_from_request, decode_jwt
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

# Define all allowed origins
origins = [
    "http://localhost:3000",  # Default React dev server
    "http://localhost:3001",  # Alternate React dev server
    "http://localhost:8000",  # Backend server
    "http://frontend",        # Docker frontend service
    "http://frontend:80",     # Docker frontend service with port
    "http://backend:8000",    # Docker backend service
    "http://backend",         # Docker backend service
]

# Set up CORS middleware with more permissive settings for separate frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth check helper function
async def is_authenticated(request: Request) -> bool:
    """Check if the request has a valid auth token."""
    token = await get_token_from_request(request)
    if not token:
        return False
    
    try:
        # Verify with JWT decoder
        decoded = decode_jwt(token)
        return decoded is not None
    except Exception as e:
        logger.debug(f"Auth check failed: {str(e)}")
        return False

# Import API routers
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
    "/api/health",
    "/api/docs",
    "/api/openapi.json",
    "/api/v1/auth"
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Custom middleware to handle API authentication."""
        path = request.url.path
        
        # Skip auth check for public paths
        if any(path.startswith(public_path) for public_path in PUBLIC_PATHS):
            return await call_next(request)
        
        # API paths require proper auth header
        if path.startswith("/api/"):
            # Let the route handler deal with authentication
            # The routes that need authentication will use the auth dependencies
            return await call_next(request)
        
        # All other paths should never be called directly in this backend-only setup
        return JSONResponse(
            status_code=404,
            content={"detail": "Not found"}
        )

# Add auth middleware
app.add_middleware(AuthMiddleware)

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