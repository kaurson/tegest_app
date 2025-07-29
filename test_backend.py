import uuid
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from app.flow.planning import PlanningFlow
from app.agent.manus import Manus

app = FastAPI(title="Estonian Learning App - Test Backend")

# Create the agent and planning flow
manus_agent = Manus()
planning_flow = PlanningFlow(agents=manus_agent)

class LessonRequest(BaseModel):
    lesson_request: str

class StepRequest(BaseModel):
    session_id: str
    step_index: int

@app.get("/")
async def read_root():
    return FileResponse("test_frontend.html")

@app.post("/api/start-lesson")
async def start_lesson(request: LessonRequest):
    try:
        session_id = str(uuid.uuid4())
        
        # Create the lesson plan
        result = await planning_flow.execute(request.lesson_request, session_id)
        
        if "Successfully created plan" in result:
            # Fetch the created plan from database
            response = planning_flow.supabase.table("Lessons").select("*").eq("session_id", session_id).execute()
            
            if response.data and len(response.data) > 0:
                plan_data = response.data[0]
                return {
                    "success": True,
                    "session_id": session_id,
                    "plan": {
                        "title": plan_data.get("title", "Untitled Plan"),
                        "description": plan_data.get("description", ""),
                        "steps": plan_data.get("steps", []),
                        "total_steps": len(plan_data.get("steps", []))
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to retrieve created plan from database"
                }
        else:
            return {
                "success": False,
                "error": result
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error creating lesson: {str(e)}"
        }

@app.post("/api/execute-step")
async def execute_step(request: StepRequest):
    try:
        # Execute the step
        result = await planning_flow._execute_step(
            manus_agent, 
            request.session_id, 
            request.step_index
        )
        
        return {
            "success": True,
            "result": result,
            "step_index": request.step_index
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error executing step: {str(e)}"
        }

@app.get("/api/lesson-status/{session_id}")
async def get_lesson_status(session_id: str):
    try:
        response = planning_flow.supabase.table("Lessons").select("*").eq("session_id", session_id).execute()
        
        if response.data and len(response.data) > 0:
            lesson_data = response.data[0]
            return {
                "success": True,
                "lesson": {
                    "title": lesson_data.get("title"),
                    "status": lesson_data.get("status"),
                    "steps": lesson_data.get("steps", []),
                    "step_statuses": lesson_data.get("step_statuses", []),
                    "step_responses": lesson_data.get("step_responses", []),
                    "progress_percentage": lesson_data.get("progress_percentage", 0)
                }
            }
        else:
            return {
                "success": False,
                "error": "Lesson not found"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching lesson status: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 