from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import os
import logging
import jwt
from jwt.exceptions import PyJWTError
import time

from app.core.supabase_client import get_supabase
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Bearer token authentication scheme
security = HTTPBearer()

# Development vs Production mode
is_production = os.environ.get("PRODUCTION", "false").lower() == "true"

# Get JWT secret from environment variable or settings
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET") or settings.SUPABASE_JWT_SECRET

def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token using the Supabase JWT secret.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        dict: The decoded token payload
        
    Raises:
        Exception: If the token is invalid or expired
    """
    if not JWT_SECRET:
        logger.warning("SUPABASE_JWT_SECRET not set, using fallback validation")
        # Fall back to verifying with Supabase API
        supabase = get_supabase()
        response = supabase.auth.get_user(token)
        return {"user": response.user, "sub": response.user.id}
    
    try:
        # Decode the JWT token using the secret
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_signature": True}
        )
        
        # Check if token is expired
        if "exp" in decoded_token and decoded_token["exp"] < time.time():
            raise Exception("Token expired")
        
        return decoded_token
    except PyJWTError as e:
        logger.error(f"Error decoding JWT: {str(e)}")
        raise Exception(f"Invalid token: {str(e)}")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get the current authenticated user from the Supabase JWT token.
    
    Args:
        credentials: The HTTP bearer token credentials from the request
        
    Returns:
        dict: The user data
        
    Raises:
        HTTPException: If the token is invalid
    """
    try:
        # Get the token from the Authorization header
        token = credentials.credentials
        
        # Decode and verify the token
        payload = decode_jwt(token)
        
        # Return the user data
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Extracts token from different sources (header, cookie, etc.)
async def get_token_from_request(request: Request) -> Optional[str]:
    """
    Extract the JWT token from various sources in the request.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        str: The extracted token, or None if not found
    """
    # First try Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")
    
    # Then try to get token from cookies
    sb_auth_token = request.cookies.get("sb-access-token")
    if sb_auth_token:
        return sb_auth_token
    
    # Finally, try query param (useful for WebSocket connections)
    token = request.query_params.get("token")
    if token:
        return token
    
    return None

# Optional auth dependency for routes that can be accessed both authenticated and unauthenticated
async def get_optional_user(
    request: Request
) -> Optional[Dict[str, Any]]:
    """
    Dependency to optionally get the current authenticated user.
    This can be used for routes that can be accessed both authenticated and unauthenticated.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        dict: The user data, or None if no valid credentials provided
    """
    token = await get_token_from_request(request)
    
    if not token:
        return None
    
    try:
        # Decode and verify the token
        payload = decode_jwt(token)
        return payload
    except Exception as e:
        logger.debug(f"Optional auth failed: {str(e)}")
        return None

# Development-only: Bypass auth when in development mode with BYPASS_AUTH=true
def dev_bypass_auth(request: Request) -> Optional[Dict[str, Any]]:
    """
    In development mode, allows bypassing auth for easier testing.
    Only works when BYPASS_AUTH=true and PRODUCTION=false
    """
    if not is_production and os.environ.get("BYPASS_AUTH", "false").lower() == "true":
        logger.warning("AUTH BYPASS ENABLED - Do not use in production!")
        return {
            "sub": "dev-user",
            "email": "dev@example.com",
            "user_metadata": {"name": "Development User"}
        }
    
    return None 