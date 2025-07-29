from fastapi import FastAPI
from app.api.fill_in_blank_router import router as fill_in_blank_router
from app.api.assessment_router import router as assessment_router
from app.api.gap_fill_router import router as gap_fill_router

app = FastAPI()

# Mount the APIs
app.include_router(fill_in_blank_router)
app.include_router(assessment_router)
app.include_router(gap_fill_router) 