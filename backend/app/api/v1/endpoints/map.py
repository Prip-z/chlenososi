from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from app.core.container import Container
from app.core.middleware import inject
from app.schema.base_schema import Blank
from app.schema.map_schema import BoundingBox, FindMap, FindMapResult, Map, MapAreaResponse, UpsertMap
from app.services.map_service import MapService

router = APIRouter(
    prefix="/maps",
    tags=["maps"],
)

@router.get("", response_model=FindMapResult)
@inject
def get_maps(
    find_query: FindMap = Depends(),
    service: MapService = Depends(Provide[Container.map_service]),
):
    return service.get_list(find_query)


@router.get("/{map_id}", response_model=Map)
@inject
def get_map(
    map_id: int,
    service: MapService = Depends(Provide[Container.map_service]),
):
    return service.get_by_id(map_id)


@router.post("", response_model=Map)
@inject
async def create_map(
    name: str = Form(...),
    pmtiles_url: str = Form(""), # Дефолтное значение, если S3 путь генерируется внутри сервиса
    description: str = Form(None),
    file: UploadFile = File(...),
    service: MapService = Depends(Provide[Container.map_service]),
):
    """
    Создание карты с загрузкой файла .pmtiles в MinIO S3
    """
    if not file.filename or not file.filename.endswith('.pmtiles'):
        raise HTTPException(status_code=400, detail="Only .pmtiles files are allowed")

    # Собираем данные в схему UpsertMap, которую ждет твой MapService
    map_data = UpsertMap(
        name=name,
        pmtiles_url=pmtiles_url,
        description=description
    )
    
    # Передаем в сервис и схему данных, и сам файл для отправки в S3
    return await service.add_with_file(map_data, file)


@router.patch("/{map_id}", response_model=Map)
@inject
def update_map(
    map_id: int,
    map_data: UpsertMap,
    service: MapService = Depends(Provide[Container.map_service]),
):
    return service.patch(map_id, map_data)


@router.delete("/{map_id}", response_model=Blank)
@inject
def delete_map(
    map_id: int,
    service: MapService = Depends(Provide[Container.map_service]),
):
    service.remove_by_id(map_id)
    return {}


@router.post("/{map_id}/download", response_model=MapAreaResponse)
@inject
def download_map_area(
    map_id: int,
    bbox: BoundingBox,
    service: MapService = Depends(Provide[Container.map_service]),
):
    return service.download_area(map_id, bbox)