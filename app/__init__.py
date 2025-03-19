# Import necessary components for the app to work
from app.core.supabase_client import supabase, get_supabase

# Import API
from app.api.v1 import api

__all__ = ["supabase", "get_supabase", "api"]
