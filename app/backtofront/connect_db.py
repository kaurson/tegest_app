from supabase import create_client, Client
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_data(table_name:str, row:str="messages", id:str = "NULL"):
    try:
        response = supabase.table(table_name).select(row).eq("session_id", id).execute()
        return response.data
    except Exception as e:
        return e
def insert_data(table_name:str = "lesson_sessions",update = "NULL", id:str = "NULL"):
    try:
        response = supabase.table(table_name).update(update).eq("session_id", id).execute()
        return response
    except Exception as e:
        return e

