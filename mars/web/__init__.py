from fastapi import APIRouter

# project imports
from .fetch_config import router as fetch_config_router
from .chat import router as chat_router
from .eval import router as eval_router


router = APIRouter()
router.include_router(fetch_config_router)
router.include_router(chat_router)
router.include_router(eval_router)
