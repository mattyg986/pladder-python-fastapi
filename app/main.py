import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {
        "message": "Welcome to Purple Ladder AI Agents Platform API",
        "docs": "/docs",
    }

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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 