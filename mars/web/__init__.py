from fastapi import APIRouter

# project imports
from .endpoints import router as endpoints_router


router = APIRouter()
router.include_router(endpoints_router)
