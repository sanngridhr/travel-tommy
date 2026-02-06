from typing import Any


from uuid import UUID

from fastapi.exceptions import HTTPException
from starlette import status
from app.database.tables import PlaceTable
from models import Place, PlaceCreate, PlaceUpdate


class PlacesService:
    def __init__(self) -> None:
        pass

    async def list_places(self) -> list[Place]:
        places: list[dict[str, Any]] = await PlaceTable.select()
        return [Place.model_validate(p) for p in places]

    async def get_place_by_id(self, id: UUID) -> Place:
        place: PlaceTable = await self.__fetch_place_by_id(id)
        return Place.model_validate(place)

    async def create_place(self, create: PlaceCreate) -> Place:
        data: dict[str, Any] = create.model_dump(exclude_unset=True)
        place: PlaceTable = await PlaceTable.objects().create(**data)
        return Place.model_validate(place.to_dict())

    async def update_place_by_id(self, id: UUID, update: PlaceUpdate) -> Place:
        data: dict[str, Any] = update.model_dump(exclude_unset=True)
        await PlaceTable.update(**data).where(PlaceTable.id == id)
        place: PlaceTable = await self.__fetch_place_by_id(id)
        return Place.model_validate(place.to_dict())

    async def delete_place_by_id(self, id: UUID) -> None:
        PlaceTable.delete().where(PlaceTable.id == id)

    async def __fetch_place_by_id(self, id: UUID) -> PlaceTable:
        place: PlaceTable | None = await PlaceTable.objects().get(PlaceTable.id == id)
        if place is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Place {id} does not exist.")
        return place
