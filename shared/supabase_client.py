import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env variables from user-service/.env or root or system environment
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user-service", ".env")
load_dotenv(env_path)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

_supabase: Client = None

def get_supabase_client() -> Client:
    global _supabase
    if _supabase is None:
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        _supabase = create_client(supabase_url, supabase_key)
    return _supabase
