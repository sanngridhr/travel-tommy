from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel, Field

from app.database.tables import ProjectTable
from app.api.v1.places.models import Place, PlaceCreate

if TYPE_CHECKING:

    class Project(BaseModel):
        id: UUID
        name: str
        description: str | None
        start_date: date | None
        is_locked = bool
        places: list[Place]

    class ProjectCreate(BaseModel):
        name: str
        description: str | None
        start_date: date | None
        is_locked = bool | None
        places: list[PlaceCreate]

    class ProjectUpdate(BaseModel):
        name: str | None
        description: str | None
        start_date: date | None
        is_locked = bool | None
else:

    class Project(
        create_pydantic_model(
            table=ProjectTable,
            include_default_columns=True,
        )
    ):
        places: list[Place] = Field(min_length=1, max_length=10)

    class ProjectCreate(
        create_pydantic_model(
            table=ProjectTable,
            exclude_columns=[ProjectTable.id],
        )
    ):
        places: list[PlaceCreate] = Field(min_length=1, max_length=10)

    class ProjectUpdate(
        create_pydantic_model(
            table=ProjectTable,
            all_optional=True,
            exclude_columns=[ProjectTable.id],
        )
    ): ...