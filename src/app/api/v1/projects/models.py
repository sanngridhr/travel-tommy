from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel, Field

from app.database.tables import ProjectTable

if TYPE_CHECKING:
    from app.api.v1.places.models import Place

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
        places: list[Place] | None

    class ProjectUpdate(BaseModel):
        name: str | None
        description: str | None
        start_date: date | None
        is_locked = bool | None
        places: list[Place] | None
else:

    class Project(
        create_pydantic_model(
            table=ProjectTable,
            include_default_columns=True,
        )
    ):
        places = list[Place] = Field(min_length=1, max_length=10)

    class ProjectCreate(
        create_pydantic_model(
            table=ProjectTable,
        )
    ):
        places = list[Place] = Field(min_length=1, max_length=10)

    class ProjectUpdate(
        create_pydantic_model(
            table=ProjectTable,
            all_optional=True,
        )
    ):
        places = list[Place] = Field(min_length=1, max_length=10) | None
