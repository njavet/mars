from fastapi import APIRouter

# project imports
from .lm import router as lm_router
from .agent import router as agent_router

router = APIRouter()
router.include_router(agent_router)
router.include_router(lm_router)
