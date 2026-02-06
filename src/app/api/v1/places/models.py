from typing import TYPE_CHECKING
from uuid import UUID
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel

from app.database.tables import PlaceTable

if TYPE_CHECKING:

    class Place(BaseModel):
        id: UUID
        title: str
        notes: str | None
        is_visited: bool
        project_id: UUID

    class PlaceCreate(BaseModel):
        title: str
        notes: str | None
        is_visited: bool

    class PlaceCreateWithProject(BaseModel):
        title: str
        notes: str | None
        is_visited: bool
        project: UUID

    class PlaceUpdate(BaseModel):
        title: str
        notes: str | None
        is_visited: bool
else:

    class Place(
        create_pydantic_model(
            table=PlaceTable,
            include_default_columns=True,
            exclude_columns=[PlaceTable.project],
        )
    ): ...

    class PlaceCreate(
        create_pydantic_model(
            table=PlaceTable,
            exclude_columns=[PlaceTable.id, PlaceTable.project],
        )
    ): ...

    class PlaceCreateWithProject(
        create_pydantic_model(
            table=PlaceTable,
            exclude_columns=[PlaceTable.id],
        )
    ): ...

    class PlaceUpdate(
        create_pydantic_model(
            table=PlaceTable,
            all_optional=True,
            exclude_columns=[PlaceTable.id, PlaceTable.project],
        )
    ): ...