import os
from fastapi import APIRouter, Header, HTTPException
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

router = APIRouter()

API_KEY = os.getenv("FLASK_API_KEY", "default-keasdfalsfjadsfkdakfkdsy")

def verify_api_key(provided_key: str) -> bool:
    return provided_key == API_KEY

@router.post("/secure-endpoint")
async def secure_route(x_api_key: str = Header(None)):
    if not verify_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Access granted"} 