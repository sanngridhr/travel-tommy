from app.api.v1.places.models import Place, PlaceCreate, PlaceCreateWithProject


from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status

from app.api.v1.places.routes import PlacesServiceDependency
from app.api.v1.projects.models import Project, ProjectCreate, ProjectUpdate
from app.api.v1.projects.service import ProjectsService


def _get_projects_service(places_service: PlacesServiceDependency) -> ProjectsService:
    return ProjectsService(places_service)


ProjectsServiceDependency = Annotated[ProjectsService, Depends(dependency=_get_projects_service)]
router = APIRouter()


@router.get("/")
async def list_projects(service: ProjectsServiceDependency) -> list[Project]:
    return await service.list_projects()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    service: ProjectsServiceDependency,
    places_service: PlacesServiceDependency,
    create: ProjectCreate,
) -> Project:
    return await service.create_project(create)


@router.get("/{id}")
async def get_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
) -> Project:
    return await service.get_project_by_id(id)


@router.put("/{id}")
@router.patch("/{id}")
async def update_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
    update: ProjectUpdate,
) -> Project:
    return await service.update_project_by_id(id, update)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
) -> None:
    return await service.delete_project_by_id(id)


@router.post("/{id}/add-place")
async def add_place_to_project(
    places_service: PlacesServiceDependency,
    id: UUID,
    place_create: PlaceCreate
) -> Place:
    data: dict[str, Any] = place_create.model_dump()
    data["project"] = id
    place_create_with_project: PlaceCreateWithProject = PlaceCreateWithProject.model_validate(data)
    return await places_service.create_place(create=place_create_with_project)