from fastapi import APIRouter
from pydantic import BaseModel

from app.schema import Message
from app.llm import LLM
# from tegus.test_rag import rag  # Uncomment when available

router = APIRouter()

class RagRequest(BaseModel):
    query: str

class RagResponse(BaseModel):
    response: str

class Teacher(BaseModel):
    query: str

@router.post("/rag")
async def get_rag(request: RagRequest):
    # TODO: Uncomment when rag function is available
    # results = rag(request.query)
    # return await results
    return {"message": "RAG endpoint - implementation pending"}

@router.post("/teacher")
async def ask_teacher(request: Teacher):
    ASK_TEACHER_POMPT = Message.system_message("""Sa oled väga hea abiõpetaja ja suudad vastata kõikidel kasutaja küsimustele. Vasta lühidalt ja otsekoheselt. Hoia vastused lihtsad ja vast kuni 10klassi teadmiste piires""")
    USER_ASK_TEACHER = Message.user_message(f"""Palun vasta minu küsimusele: {request.query}""")
    opetaja = LLM()
    return await opetaja.ask(
        messages=[USER_ASK_TEACHER],
        system_msgs=[ASK_TEACHER_POMPT]
    ) 