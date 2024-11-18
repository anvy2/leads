


from fastapi import APIRouter
from src.api.routers import lead

router = APIRouter(prefix="/public", tags=["public"])

router.include_router(lead.router)
