from uuid import UUID
from schemas import Project, ProjectCreate, ProjectUpdate


class ProjectsService:
    def __init__(self) -> None:
        pass

    async def list_projects(self) -> list[Project]: ...

    async def get_project_by_id(self, id: UUID) -> Project: ...

    async def create_project(self, create: ProjectCreate) -> Project: ...

    async def update_project_by_id(self, id: UUID, update: ProjectUpdate) -> Project: ...

    async def delete_project_by_id(self, id: UUID) -> None: ...
