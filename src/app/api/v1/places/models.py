from typing import TYPE_CHECKING
from uuid import UUID
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel

from app.api.v1.projects.models import Project
from app.database.tables import PlaceTable

if TYPE_CHECKING:

    class Place(BaseModel):
        id: UUID
        foreign_id: int
        title: str
        notes: str | None
        is_visited: bool
        project: Project

    class PlaceCreate(BaseModel):
        title: str
        notes: str | None
        is_visited: bool
        projects: Project

    class PlaceUpdate(BaseModel):
        foreign_id: int 
        title: str
        notes: str | None
        is_visited: bool
        projects: Project
else:

    class Place(
        create_pydantic_model(
            table=PlaceTable,
            nested=True,
            include_default_columns=True,
        )
    ): ...

    class PlaceCreate(
        create_pydantic_model(
            table=PlaceTable,
            nested=True,
        )
    ): ...

    class PlaceUpdate(
        create_pydantic_model(
            table=PlaceTable,
            nested=True,
            all_optional=True,
        )
    ):
        id: UUID
