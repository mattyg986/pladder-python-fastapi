import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
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
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

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

# Serve static files for production React frontend
@app.get("/{catch_all:path}")
async def serve_frontend(catch_all: str, request: Request):
    """Serve frontend for all other routes in production."""
    if not is_production or not static_dir.exists():
        return JSONResponse({"detail": "Not found"}, status_code=404)
    
    # Check if the path exists as a static file
    static_file = static_dir / catch_all
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # Fallback to index.html for client-side routing
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