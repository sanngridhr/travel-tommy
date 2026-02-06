from typing import Any


from uuid import UUID

from fastapi.exceptions import HTTPException
from starlette import status
from app.database.tables import PlaceTable, ProjectTable, ProjectToPlace
from models import Project, ProjectCreate, ProjectUpdate


class ProjectsService:
    def __init__(self) -> None:
        pass

    async def list_projects(self) -> list[Project]:
        projects: list[dict[str, Any]] = await ProjectTable.select()
        return [Project.model_validate(p) for p in projects]

    async def get_project_by_id(self, id: UUID) -> Project:
        project: ProjectTable = await self.__fetch_project_by_id(id)
        return Project.model_validate(project)

    async def create_project(self, create: ProjectCreate) -> Project:
        data: dict[str, Any] = create.model_dump(exclude_unset=True)
        project: ProjectTable = await ProjectTable.objects().create(**data)
        return Project.model_validate(project.to_dict())

    async def update_project_by_id(self, id: UUID, update: ProjectUpdate) -> Project:
        data: dict[str, Any] = update.model_dump(exclude_unset=True)
        await ProjectTable.update(**data).where(ProjectTable.id == id)
        project: ProjectTable = await self.__fetch_project_by_id(id)
        return Project.model_validate(project.to_dict())

    async def delete_project_by_id(self, id: UUID) -> None:
        is_locked = await self.__check_project_lock_by_id(id)
        if is_locked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project {id} is locked (has visited places), cannot delete.",
            )
        ProjectTable.delete().where(ProjectTable.id == id)

    async def __check_project_lock_by_id(self, id: UUID) -> bool:
        return await ProjectToPlace.exists().where(
            (ProjectToPlace.project == id)
            & (ProjectToPlace.place.is_in(PlaceTable.select(PlaceTable.id).where(PlaceTable.is_visited == True)))  # noqa: E712
        )

    async def __fetch_project_by_id(self, id: UUID) -> ProjectTable:
        project: ProjectTable | None = await ProjectTable.objects().get(ProjectTable.id == id)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {id} does not exist.")
        return project
