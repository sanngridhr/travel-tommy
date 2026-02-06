from datetime import date
from pydantic import BaseModel, Field

from app.api.v1.places.schemas.place import Place


class ProjectUpdate(BaseModel):
    name: str | None
    description: str | None
    start_date: date | None
    places: list[Place] | None = Field(min_length=1, max_length=10)
