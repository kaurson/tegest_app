import os
import asyncio
from fastapi import FastAPI, Header, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv, find_dotenv
import logging
from supabase import create_client, Client
from pydantic import BaseModel, Field
import time
from typing import Dict, List, Optional, Union
import uuid
import json
from fastapi.middleware.cors import CORSMiddleware



from app.schema import Message
from app.agent.manus import Manus
from app.tool import ToolCollection
from app.flow.base import FlowType
from app.flow.flow_factory import FlowFactory
from app.logger import logger
from app.backtofront.connect_db import get_data
from app.flow.planning import PlanningFlow
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.web_search import WebSearch
from app.tool.rag_model import RagSearch
from app.agent.base import BaseAgent
from app.tool.test_rag import rag
from app.llm import LLM

load_dotenv(find_dotenv())

logging.basicConfig(filename='/opt/logs/record.log', level=logging.DEBUG)
app = FastAPI()
# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

API_KEY = os.getenv("FLASK_API_KEY", "default-keasdfalsfjadsfkdakfkdsy")

def verify_api_key(provided_key: str) -> bool:
    return provided_key == API_KEY

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")



supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




@app.get("/")
async def index():
    logger.debug("debug log info")
    logger.info("Info log information")
    logger.warning("Warning log info")
    logger.error("Error log info")
    logger.critical("Critical log info")
    return {"message": "Hello from FastAPI"}
@app.post("/secure-endpoint")
async def secure_route(x_api_key: str = Header(None)):
    if not verify_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Access granted"}



class PlanRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = Field(default_factory=lambda: f"session_{int(time.time())}")

class StepRequest(BaseModel):
    step_id:int
    session_id: str

class SimpleAgent(BaseAgent):
    """A simple concrete implementation of BaseAgent."""
    
    async def step(self) -> str:
        """Implementation of the abstract step method."""
        # Use the last message in memory or a default message
        last_message = self.memory.messages[-1].content if self.memory.messages else "No input"
        
        # If the message starts with "Please provide a direct answer to:", remove that part
        if last_message.startswith("Please provide a direct answer to:"):
            task = last_message.replace("Please provide a direct answer to:", "").strip()
            return f"Here's the answer to your question: {task}"
            
        return last_message


    

# Response model to include session_id
class PlanResponse(BaseModel):
    session_id: str
    plan: str
simple_agent = SimpleAgent(name="SimpleAgent")
agents = {"manus": Manus()}


# API Endpoints
@app.post("/create-plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest):
    flow = FlowFactory.create_flow(
            flow_type=FlowType.PLANNING,
            agents=agents,
        )
    session_id = str(uuid.uuid4())  # Generate UUID
    plan_text = await flow.execute(input_text=request.prompt, session_id=session_id)
    return PlanResponse(session_id=session_id, plan=plan_text)


async def run_execute(session_id:str, step_id:int):
    agents = {"manus": Manus()}
    planning_flow = PlanningFlow(agents=agents)
    return await planning_flow._execute_step(executor=agents,session_id=session_id, step_id=step_id)



@app.post("/execute-step", response_model=str)
async def execute_step(request: StepRequest, background_task:BackgroundTasks):
    try:
        background_task.add_task(run_execute, session_id=request.session_id, step_id=request.step_id)
        response = {"session_id":request.session_id,
                    "step":request.step_id,
                    "status":"completed"}
        return json.dumps(response)
        
    except Exception as e:
        logger.error(f"Error executing step: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    


class RagRequest(BaseModel):
    query: str
class RagResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the backend is running properly
    """
    try:
        # Basic health check - you can add more sophisticated checks here
        # like database connectivity, external service availability, etc.
        return {
            "status": "healthy",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "service": "Tegus Backend API",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")



@app.post("/rag")
async def get_rag(request:RagRequest):
    results = rag(request.query)
    return await results


class Teacher(BaseModel):
    query:str
@app.post("/teacher")
async def ask_teacher(request:Teacher):
    ASK_TEACHER_POMPT = Message.system_message("""Sa oled väga hea abiõpetaja ja suudad vastata kõikidel kasutaja küsimustele. Vasta lühidalt ja otsekoheselt. Hoia vastused lihtsad ja vast kuni 10klassi teadmiste piires""")
    USER_ASK_TEACHER = Message.user_message(f"""Palun vasta minu küsimusele: {request.query}""")
    opetaja = LLM()
    return await opetaja.ask(
        messages=[USER_ASK_TEACHER],
        system_msgs=[ASK_TEACHER_POMPT]
    )

