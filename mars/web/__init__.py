from fastapi import APIRouter

# project imports
from .agent import router as agent_router

router = APIRouter()
router.include_router(agent_router)
