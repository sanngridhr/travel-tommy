from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from app.api.v1.projects.schemas import Project, ProjectCreate, ProjectUpdate
from app.api.v1.projects.service import ProjectsService

PROJECTS_PATH = "/projects"
router = APIRouter()


def _get_projects_service() -> ProjectsService:
    return ProjectsService()


ProjectsServiceDependency = Annotated[ProjectsService, Depends(dependency=_get_projects_service)]


@router.get(PROJECTS_PATH)
async def list_projects(service: ProjectsServiceDependency) -> list[Project]:
    return await service.list_projects()


@router.post(PROJECTS_PATH)
async def create_project(service: ProjectsServiceDependency, create: ProjectCreate) -> Project:
    return await service.create_project(create)


@router.get(PROJECTS_PATH + "{project_id}")
async def get_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
) -> Project:
    return await service.get_project_by_id(id)


@router.put(PROJECTS_PATH + "{project_id}")
@router.patch(PROJECTS_PATH + "{project_id}")
async def update_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
    update: ProjectUpdate,
) -> Project:
    return await service.update_project_by_id(id, update)


@router.delete(PROJECTS_PATH + "{project_id}")
async def delete_project_by_id(
    service: ProjectsServiceDependency,
    id: UUID,
) -> None:
    return await service.delete_project_by_id(id)
