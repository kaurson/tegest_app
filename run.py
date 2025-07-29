import os
import asyncio
import datetime
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

# Import API routes
from api.routes.core import router as core_router
from api.routes.auth import router as auth_router
from api.routes.planning import router as planning_router
from api.routes.ai import router as ai_router
from api.routes.user import router as user_router

from app.schema import Message
from app.agent.manus import Manus
from app.tool import ToolCollection
from app.flow.base import FlowType
from app.flow.flow_factory import FlowFactory
from app.logger import logger
from app.backtofront.connect_db import get_data
from app.flow.planning import PlanningFlow
#from tegus.web_search import WebSearch
#from tegus.rag_model import RagSearch
from app.agent.base import BaseAgent
#from tegus.test_rag import rag
from app.llm import LLM

load_dotenv(find_dotenv())

# Create logs directory if it doesn't exist
import os
os.makedirs('logs', exist_ok=True)

logging.basicConfig(filename='logs/record.log', level=logging.DEBUG)
app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(core_router, tags=["core"])
app.include_router(auth_router, tags=["auth"])
app.include_router(planning_router, tags=["planning"])
app.include_router(ai_router, tags=["ai"])
app.include_router(user_router, tags=["users"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

simple_agent = SimpleAgent(name="SimpleAgent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)

