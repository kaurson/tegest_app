from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.tool.fill_in_blank import FillInTheBlankTool

router = APIRouter()
fill_tool = FillInTheBlankTool()

class GenerateRequest(BaseModel):
    text: str
    num_blanks: int = 5

class CheckRequest(BaseModel):
    user_answers: list[str]
    correct_answers: list[str]

@router.post("/api/fill-in-blank/generate")
async def generate_exercise(data: GenerateRequest):
    result = await fill_tool.execute(text=data.text, num_blanks=data.num_blanks)
    return result

@router.post("/api/fill-in-blank/check")
async def check_exercise(data: CheckRequest):
    result = await fill_tool.execute(
        text="",  # Not needed for checking
        user_answers=data.user_answers,
        correct_answers=data.correct_answers
    )
    return result 