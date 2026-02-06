from typing import Any


from uuid import UUID
from app.database.tables import PlaceTable, ProjectTable
from models import Project, ProjectCreate, ProjectUpdate


class ProjectsService:
    def __init__(self) -> None:
        pass

    async def list_projects(self) -> list[Project]:
        projects: list[dict[str, Any]] = await ProjectTable.select()
        return [Project.model_validate(p) for p in projects]

    async def get_project_by_id(self, id: UUID) -> Project:
        project: list[dict[str, Any]] = await ProjectTable.select().where(ProjectTable.id == id)
        return Project.model_validate(project)

    async def create_project(self, create: ProjectCreate) -> Project:
        if not create.is_locked:
            PlaceTable.objects.where(create in PlaceTable.projects)
        project: ProjectTable = ProjectTable(**create.model_dump())
        await project.save()
        return Project.model_validate(project.to_dict())

    async def update_project_by_id(self, update: ProjectUpdate) -> Project:
        project = ProjectTable(**update.model_dump())
        await project.save()
        return Project.model_validate(project.to_dict())


    async def delete_project_by_id(self, id: UUID) -> None: ...
