from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status

from app.api.v1.projects.models import Project, ProjectCreate, ProjectUpdate
from app.api.v1.projects.service import ProjectsService



def _get_projects_service() -> ProjectsService:
    return ProjectsService()


ProjectsServiceDependency = Annotated[ProjectsService, Depends(dependency=_get_projects_service)]
router = APIRouter()


@router.get("/")
async def list_projects(service: ProjectsServiceDependency) -> list[Project]:
    return await service.list_projects()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(service: ProjectsServiceDependency, create: ProjectCreate) -> Project:
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
