from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import random
from supabase import create_client
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

class GapFillCheckRequest(BaseModel):
    exercise_id: int
    user_answers: list[str]

@router.get("/api/gap-fill-exercise")
def get_gap_fill_exercise():
    response = supabase.table("gap_fill_exercises").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="No exercises found")
    exercises = response.data
    exercise = random.choice(exercises)
    return exercise

@router.post("/api/gap-fill-check")
def check_gap_fill(data: GapFillCheckRequest):
    resp = supabase.table("gap_fill_exercises").select("answers").eq("id", data.exercise_id).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    correct = resp.data[0]["answers"]
    # correct and user_answers are both lists
    score = 0
    feedback = []
    for i, (u, c) in enumerate(zip(data.user_answers, correct)):
        if u.strip().lower() == c.strip().lower():
            score += 1
            feedback.append(f"{i+1}. Õige")
        else:
            feedback.append(f"{i+1}. Vale (õige: {c})")
    return {"score": score, "total": len(correct), "feedback": feedback} 