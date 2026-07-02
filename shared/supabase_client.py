# import os
# from supabase import create_client, Client
# from dotenv import load_dotenv
 
# # Load environment variables (useful if called from a script directly)
# load_dotenv()
 
# def get_supabase_client() -> Client:
#     url: str = os.environ.get("SUPABASE_URL")
#     key: str = os.environ.get("SUPABASE_KEY")
   
#     if not url or not key:
#         raise ValueError("Supabase URL and Key must be provided in environment variables")
       
#     return create_client(url, key)
 
# supabase: Client = get_supabase_client()
 
import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from supabase import create_client, Client
 
print("Current working directory:", os.getcwd())
print("This file:", __file__)
 
dotenv_path = Path(__file__).resolve().parent.parent / "audit-service" / ".env"
print("Loading .env from:", dotenv_path)
 
load_dotenv(dotenv_path)
 
print("SUPABASE_URL =", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY exists =", os.getenv("SUPABASE_KEY") is not None)
 
 
def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
 
    if not url or not key:
        raise ValueError("Supabase URL and Key must be provided in environment variables")
 
    return create_client(url, key)
 
supabase = get_supabase_client()