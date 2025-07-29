import json
import uuid
import time
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from app.agent.manus import Manus
from app.flow.base import FlowType
from app.flow.flow_factory import FlowFactory
from app.flow.planning import PlanningFlow
from app.logger import logger

router = APIRouter()

class PlanRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = Field(default_factory=lambda: f"session_{int(time.time())}")

class StepRequest(BaseModel):
    step_id: int
    session_id: str

class PlanResponse(BaseModel):
    session_id: str
    plan: str

agents = {"manus": Manus()}

@router.post("/create-plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest):
    flow = FlowFactory.create_flow(
        flow_type=FlowType.PLANNING,
        agents=agents,
    )
    session_id = str(uuid.uuid4())  # Generate UUID
    plan_text = await flow.execute(input_text=request.prompt, session_id=session_id)
    return PlanResponse(session_id=session_id, plan=plan_text)

async def run_execute(session_id: str, step_id: int):
    agents = {"manus": Manus()}
    planning_flow = PlanningFlow(agents=agents)
    return await planning_flow._execute_step(executor=agents, session_id=session_id, step_id=step_id)

@router.post("/execute-step", response_model=str)
async def execute_step(request: StepRequest, background_task: BackgroundTasks):
    try:
        background_task.add_task(run_execute, session_id=request.session_id, step_id=request.step_id)
        response = {
            "session_id": request.session_id,
            "step": request.step_id,
            "status": "completed"
        }
        return json.dumps(response)
        
    except Exception as e:
        logger.error(f"Error executing step: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 