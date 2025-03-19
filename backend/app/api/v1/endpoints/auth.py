from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
import os
from app.core.auth import get_current_user, get_optional_user

router = APIRouter()

@router.get("/me")
async def get_user_info(
    user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Protected endpoint that returns the current user's information.
    This endpoint is only accessible with a valid JWT token.
    """
    return {
        "id": user.get("id"),
        "email": user.get("email"),
        "user_metadata": user.get("user_metadata", {}),
        "app_metadata": user.get("app_metadata", {})
    }

@router.get("/public-data")
async def get_public_data(
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Public endpoint that returns different data based on authentication status.
    This endpoint can be accessed with or without a valid JWT token.
    """
    if user is None:
        return {"message": "This is public data that anyone can access"}
    
    return {
        "message": "This is public data with user context",
        "user_id": user.get("id"),
        "email": user.get("email")
    }

@router.get("/config")
async def get_auth_config() -> Dict[str, str]:
    """
    Public endpoint that returns the Supabase configuration for the frontend.
    This allows the frontend to access the Supabase URL and anonymous key.
    """
    return {
        "supabaseUrl": os.environ.get("SUPABASE_URL", ""),
        "supabaseAnonKey": os.environ.get("SUPABASE_KEY", "")
    } 