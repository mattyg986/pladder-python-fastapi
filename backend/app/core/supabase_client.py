import os
import logging
from supabase import create_client, Client

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create a Supabase client
try:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    logger.info(f"Supabase client created with URL: {settings.SUPABASE_URL}")
except Exception as e:
    logger.error(f"Error creating Supabase client: {str(e)}")
    # Create a placeholder client for error handling
    supabase = None

def get_supabase() -> Client:
    """
    Returns a Supabase client instance.
    This function is used as a dependency to ensure consistent client access.
    """
    if supabase is None:
        raise Exception("Supabase client not initialized")
    return supabase 