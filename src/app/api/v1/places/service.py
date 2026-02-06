from sqlite3 import IntegrityError
from typing import Any


from uuid import UUID

import aiohttp
from fastapi.exceptions import HTTPException
from starlette import status
from app.database.tables import PlaceTable
from app.api.v1.places.models import Place, PlaceCreate, PlaceCreateWithProject, PlaceUpdate


class PlacesService:
    def __init__(self):
        self._aiohttp_session = aiohttp.ClientSession()

    # --- PUBLIC API --- #

    async def list_places(self) -> list[Place]:
        places: list[dict[str, Any]] = await PlaceTable.select()
        return [Place.model_validate(p) for p in places]

    async def get_place_by_id(self, id: UUID) -> Place:
        place: PlaceTable = await self.__fetch_place_by_id(id)
        return Place.model_validate(place)

    async def create_place(self, create: PlaceCreate | PlaceCreateWithProject) -> Place:
        data: dict[str, Any] = create.model_dump(exclude_unset=True)
        data["foreign_id"] = await self.__get_foreign_id(create)
        try:
            place: PlaceTable = await PlaceTable.objects().create(**data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{create.title} already exists on the same project"
            ) from e
        return Place.model_validate(place.to_dict())

    async def update_place_by_id(self, id: UUID, update: PlaceUpdate) -> Place:
        data: dict[str, Any] = update.model_dump(exclude_unset=True)
        data["foreign_id"] = await self.__get_foreign_id(update)
        try:
            await PlaceTable.update(**data).where(PlaceTable.id == id)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{update.title} already exists on the same project"
            ) from e
        place: PlaceTable = await self.__fetch_place_by_id(id)
        return Place.model_validate(place.to_dict())

    async def delete_place_by_id(self, id: UUID) -> None:
        PlaceTable.delete().where(PlaceTable.id == id)

    # --- HELPER FUNCTION(S) --- #

    async def __fetch_place_by_id(self, id: UUID) -> PlaceTable:
        place: PlaceTable | None = await PlaceTable.objects().get(PlaceTable.id == id)
        if place is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Place {id} does not exist.")
        return place

    async def __get_foreign_id(
        self,
        place: PlaceCreate | PlaceCreateWithProject | PlaceUpdate,
    ) -> int:
        base_url = "https://api.artic.edu/api/v1/places/search"
        async with self._aiohttp_session.get(f"{base_url}?q={place.title}") as response:
            places: dict[str, Any] = await response.json()
            data: list[dict[str, int | str]] = places["data"]

        if len(data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Place {place.title} not found on external API {base_url}"
            )

        return data[0]["id"]  # pyright: ignore[reportReturnType]