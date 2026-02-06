from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status

from app.api.v1.places.models import Place, PlaceCreate, PlaceUpdate
from app.api.v1.places.service import PlacesService

PLACES_PATH = "/places"
router = APIRouter()


def _get_places_service() -> PlacesService:
    return PlacesService()


PlacesServiceDependency = Annotated[PlacesService, Depends(dependency=_get_places_service)]


@router.get(PLACES_PATH)
async def list_places(service: PlacesServiceDependency) -> list[Place]:
    return await service.list_places()


@router.post(PLACES_PATH, status_code=status.HTTP_201_CREATED)
async def create_place(service: PlacesServiceDependency, create: PlaceCreate) -> Place:
    return await service.create_place(create)


@router.get(PLACES_PATH + "{id}")
async def get_place_by_id(
    service: PlacesServiceDependency,
    id: UUID,
) -> Place:
    return await service.get_place_by_id(id)


@router.put(PLACES_PATH + "{id}")
@router.patch(PLACES_PATH + "{id}")
async def update_place_by_id(
    service: PlacesServiceDependency,
    id: UUID,
    update: PlaceUpdate,
) -> Place:
    return await service.update_place_by_id(id, update)


@router.delete(PLACES_PATH + "{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place_by_id(
    service: PlacesServiceDependency,
    id: UUID,
) -> None:
    return await service.delete_place_by_id(id)
