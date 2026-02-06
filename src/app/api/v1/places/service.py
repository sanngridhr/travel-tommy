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
        await self.__validate_place_with_external_endpoint(create)
        data: dict[str, Any] = create.model_dump(exclude_unset=True)
        place: PlaceTable = await PlaceTable.objects().create(**data)
        return Place.model_validate(place.to_dict())

    async def update_place_by_id(self, id: UUID, update: PlaceUpdate) -> Place:
        await self.__validate_place_with_external_endpoint(update)
        data: dict[str, Any] = update.model_dump(exclude_unset=True)
        await PlaceTable.update(**data).where(PlaceTable.id == id)
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

    async def __validate_place_with_external_endpoint(
        self,
        place: PlaceCreate | PlaceCreateWithProject | PlaceUpdate,
    ) -> None:
        base_url = "https://api.artic.edu/api/v1/places/search"
        async with self._aiohttp_session.get(f"{base_url}?q={place.title}") as response:
            data: dict[str, Any] = await response.json()
            results: list[dict] = data["data"]

            if len(results) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Place {place.title} not found on {base_url}"
                )
        return