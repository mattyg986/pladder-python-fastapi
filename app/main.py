import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
import pathlib

from app.core.config import settings
from app.core.init_db import init_db, create_initial_data
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

# Import API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Check if we're in a production environment
is_production = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PRODUCTION")

# Handle production static files (built React app)
static_dir = pathlib.Path(__file__).parent / "static"
if is_production and static_dir.exists():
    logger.info(f"Serving static files from {static_dir}")
    
    # React creates a nested static directory structure when built:
    # app/static/static/js/main.js
    # app/static/static/css/main.css
    # We need to mount the inner static directory to /static to serve these files correctly
    nested_static_dir = static_dir / "static"
    if nested_static_dir.exists():
        logger.info(f"Serving nested static files from {nested_static_dir}")
        app.mount("/static", StaticFiles(directory=str(nested_static_dir)), name="static")

@app.get("/")
async def root(request: Request):
    """Root endpoint - either returns API info or serves frontend."""
    if is_production and static_dir.exists():
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    
    return {
        "message": "Welcome to Purple Ladder AI Agents Platform API",
        "docs": "/docs",
    }

# The following handlers serve static files from the root level of the React build
# These are necessary because these files are referenced directly from index.html
# and are not under the /static path

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon.ico from static directory."""
    if is_production and static_dir.exists():
        favicon_path = static_dir / "favicon.ico"
        if favicon_path.exists():
            return FileResponse(favicon_path)
    return JSONResponse({"detail": "Not found"}, status_code=404)

@app.get("/manifest.json")
async def manifest():
    """Serve manifest.json from static directory."""
    if is_production and static_dir.exists():
        manifest_path = static_dir / "manifest.json"
        if manifest_path.exists():
            return FileResponse(manifest_path)
    return JSONResponse({"detail": "Not found"}, status_code=404)

@app.get("/logo192.png")
async def logo192():
    """Serve logo192.png from static directory."""
    if is_production and static_dir.exists():
        logo_path = static_dir / "logo192.png"
        if logo_path.exists():
            return FileResponse(logo_path)
    return JSONResponse({"detail": "Not found"}, status_code=404)

@app.get("/logo512.png")
async def logo512():
    """Serve logo512.png from static directory."""
    if is_production and static_dir.exists():
        logo_path = static_dir / "logo512.png"
        if logo_path.exists():
            return FileResponse(logo_path)
    return JSONResponse({"detail": "Not found"}, status_code=404)

# Serve static files for production React frontend and handle client-side routing
@app.get("/{catch_all:path}")
async def serve_frontend(catch_all: str, request: Request):
    """Serve frontend for all other routes in production."""
    if not is_production or not static_dir.exists():
        return JSONResponse({"detail": "Not found"}, status_code=404)
    
    # First check if this is a static file that needs to be served
    static_file = static_dir / catch_all
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # If not a static file, serve index.html to support client-side routing in React
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    return JSONResponse({"detail": "Not found"}, status_code=404)

@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    # Initialize the database
    init_db()
    create_initial_data()
    
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

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=not is_production
    ) 