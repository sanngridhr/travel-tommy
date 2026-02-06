from uuid import UUID
from pydantic import BaseModel


class Place(BaseModel):
    id: UUID
    foreign_id: int
    title: str
    notes: str | None
    is_visited: bool = False
