from fastapi import APIRouter, Depends

from app.core.config import settings

router = APIRouter()

@router.get("/", summary="Health check endpoint")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "api_version": "v1",
        "service": settings.PROJECT_NAME,
    } 