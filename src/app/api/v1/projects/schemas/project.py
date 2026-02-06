from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field

from app.api.v1.places.schemas.place import Place


class Project(BaseModel):
    id: UUID
    name: str
    description: str | None
    start_date: date | None
    places: list[Place] = Field(min_length=1, max_length=10)
    is_locked: bool = False
