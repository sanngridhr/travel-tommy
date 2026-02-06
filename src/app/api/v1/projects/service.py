from typing import Any


from uuid import UUID

from fastapi import HTTPException, status

from app.api.v1.places.routes import PlacesServiceDependency
from app.api.v1.projects.models import Project, ProjectCreate, ProjectUpdate
from app.api.v1.places.models import Place, PlaceCreateWithProject
from app.database.tables import ProjectTable, PlaceTable


class ProjectsService:
    def __init__(self, places_service: PlacesServiceDependency):
        self.places_service = places_service

    # --- PUBLIC API --- #

    async def list_projects(self) -> list[Project]:
        projects: list[ProjectTable] = await ProjectTable.objects()

        return [await self.__to_pydantic_model(project) for project in projects]

    async def get_project_by_id(self, id: UUID) -> Project:
        project: ProjectTable = await self.__fetch_project_by_id(id)
        return await self.__to_pydantic_model(project)

    async def create_project(self, create: ProjectCreate) -> Project:
        data: dict[str, Any] = create.model_dump(exclude_unset=True, exclude={"places"})
        project: ProjectTable = await ProjectTable.objects().create(**data)

        for place in create.places:
            place_data: dict[str, Any] = place.model_dump()
            place_data["project"] = project.id
            create_place = PlaceCreateWithProject.model_validate(place_data)
            await self.places_service.create_place(create_place)

        return await self.__to_pydantic_model(project)

    async def update_project_by_id(self, id: UUID, update: ProjectUpdate) -> Project:
        data: dict[str, Any] = update.model_dump(exclude_unset=True)
        await ProjectTable.update(**data).where(ProjectTable.id == id)
        project: ProjectTable = await self.__fetch_project_by_id(id)
        return await self.__to_pydantic_model(project)

    async def delete_project_by_id(self, id: UUID) -> None:
        if await self.__check_project_lock(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project {id} is locked (has visited some places).",
            )

        await ProjectTable.delete().where(ProjectTable.id == id).run()

    # --- HELPER FUNCTIONS --- #

    async def __fetch_project_by_id(self, id: UUID) -> ProjectTable:
        project: ProjectTable | None = await ProjectTable.objects().get(ProjectTable.id == id)

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {id} does not exist.",
            )

        return project

    async def __to_pydantic_model(self, project: ProjectTable) -> Project:
        places: list[PlaceTable] = await PlaceTable.objects().where(PlaceTable.project == project.id)

        return Project(
            **project.to_dict(),
            places=[Place.model_validate(p.to_dict()) for p in places],
        )

    async def __check_project_lock(self, id: UUID) -> bool:
        return await PlaceTable.exists().where(
            (PlaceTable.project == id) & (PlaceTable.is_visited == True)  # noqa: E712
        )
