from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.middleware import inject
from app.schema.map_schema import BoundingBox, MapAreaResponse
from app.services.map_service import MapService

router = APIRouter(
    prefix="/maps",
    tags=["maps"],
)

@router.post("/{map_id}/download", response_model=MapAreaResponse)
@inject
def download_map_area(
    map_id: int,
    bbox: BoundingBox,
    service: MapService = Depends(Provide[Container.map_service]),
):
    return service.download_area(map_id, bbox)