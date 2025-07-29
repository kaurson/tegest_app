import datetime
from fastapi import APIRouter, HTTPException
from app.logger import logger

router = APIRouter()

@router.get("/")
async def index():
    logger.debug("debug log info")
    logger.info("Info log information")
    logger.warning("Warning log info")
    logger.error("Error log info")
    logger.critical("Critical log info")
    return {"message": "Hello from FastAPI"}

@router.get("/health")
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