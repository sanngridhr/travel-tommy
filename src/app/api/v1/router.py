from fastapi.routing import APIRouter

from app.api.v1.places.routes import router as places_router
from app.api.v1.projects.routes import router as projects_router

v1_router: APIRouter = APIRouter(prefix="/v1")
v1_router.include_router(router=projects_router, prefix="/projects", tags=["projects"])
v1_router.include_router(router=places_router, prefix="/places", tags=["places"])
