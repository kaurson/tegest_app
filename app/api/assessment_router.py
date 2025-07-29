from fastapi import APIRouter, HTTPException, Request
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

class AssessmentAnswer(BaseModel):
    user_id: str
    answers: list  # [{id, selected_option}]

@router.get("/api/assessment-exercises")
def get_assessment_exercises():
    response = supabase.table("assessment_exercises").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="No exercises found")
    exercises = response.data
    random.shuffle(exercises)
    return exercises[:3]

@router.post("/api/assessment-submit")
def submit_assessment(data: AssessmentAnswer):
    # Fetch correct answers
    ids = [a["id"] for a in data.answers]
    resp = supabase.table("assessment_exercises").select("id, answer").in_("id", ids).execute()
    correct_map = {str(row["id"]): row["answer"] for row in resp.data}
    score = 0
    for a in data.answers:
        if str(a["id"]) in correct_map and a["selected_option"] == correct_map[str(a["id"])]:
            score += 1
    # Save result
    result = {
        "user_id": data.user_id,
        "answers": data.answers,
        "score": score,
    }
    supabase.table("user_assessments").insert(result).execute()
    return {"score": score, "total": len(data.answers)} 