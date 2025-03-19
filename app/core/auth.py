from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.core.supabase import get_supabase_client

# Bearer token authentication scheme
security = HTTPBearer()

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
        
        # Verify the JWT token with Supabase
        supabase = get_supabase_client()
        
        # Use the token to get the user
        response = supabase.auth.get_user(token)
        
        # Return the user data
        return response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Optional auth dependency for routes that can be accessed both authenticated and unauthenticated
async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    """
    Dependency to optionally get the current authenticated user.
    This can be used for routes that can be accessed both authenticated and unauthenticated.
    
    Args:
        credentials: The HTTP bearer token credentials from the request (optional)
        
    Returns:
        dict: The user data, or None if no valid credentials provided
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        supabase = get_supabase_client()
        response = supabase.auth.get_user(token)
        return response.user
    except:
        return None 