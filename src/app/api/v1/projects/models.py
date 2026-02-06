from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel

from app.api.v1.places.models import Place
from app.database.tables import ProjectTable

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
            nested=True,
            include_default_columns=True,
        )
    ): ...

    class ProjectCreate(
        create_pydantic_model(
            table=ProjectTable,
            nested=True,
        )
    ): ...

    class ProjectUpdate(
        create_pydantic_model(
            table=ProjectTable,
            nested=True,
            all_optional=True,
        )
    ):
        id: UUID
