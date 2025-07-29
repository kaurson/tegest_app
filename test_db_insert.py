import os
from supabase import create_client
import uuid

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

plan_data = {
    "session_id": str(uuid.uuid4()),
    "user_id": "test_user",
    "title": "Test",
    "description": "Test",
    "steps": ["step1"],
    "step_statuses": ["not_started"],
    "step_responses": [
        {
            "step_index": 0,
            "status": "not_started",
            "content": {
                "timestamp": "",
                "type": "",
                "content": "",
                "tool_type": ""
            }
        }
    ],
    "current_step_index": 0,
    "status": "not_started"
}

print("Attempting to insert:")
print(plan_data)
print("Type of step_responses:", type(plan_data["step_responses"]))

try:
    result = supabase.table("Lessons").insert(plan_data).execute()
    print("Insert result:", result)
except Exception as e:
    print("Insert error:", e) 