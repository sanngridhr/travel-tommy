from typing import Literal


from fastapi import APIRouter

from app.api.v1.router import v1_router


router: APIRouter = APIRouter(prefix="/api")
router.include_router(v1_router, prefix="/v1")

@router.get("/health")
async def health() -> Literal["OK"]:
    return "OK"