from app.repository.map_repository import MapRepository
from app.services.base_service import BaseService
from app.schema.map_schema import BoundingBox, Map, MapAreaResponse
from app.core.exceptions import NotFoundError
import uuid
from app.core.s3 import s3_storage
from app.schema.map_schema import UpsertMap

from app.schema.map_schema import NodeResponse, EdgeResponse, MapAreaResponse, BoundingBox
from app.core.exceptions import NotFoundError # или откуда у тебя NotFoundError

class MapService(BaseService):
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository
        super().__init__(map_repository)

    def download_area(self, map_id: int, bbox: BoundingBox) -> MapAreaResponse:
        map_info = self.get_by_id(map_id)
        if not map_info:
            raise NotFoundError("Карта не найдена")

        nodes_data = self.map_repository.get_nodes_in_bbox(
            map_id, bbox.min_lon, bbox.min_lat, bbox.max_lon, bbox.max_lat
        )

        node_ids = [node['id'] for node in nodes_data]
        
        edges_data = []
        if node_ids:
            edges_data = self.map_repository.get_edges_by_node_ids(map_id, node_ids)

        validated_nodes = [NodeResponse(**node) for node in nodes_data]
        
        validated_edges = [EdgeResponse.from_orm(edge) for edge in edges_data]

        return MapAreaResponse(
            map_id=map_info.id,
            pmtiles_url=map_info.pmtiles_url,
            nodes=validated_nodes, 
            edges=validated_edges   
        )
    
    async def add_with_file(self, map_data: UpsertMap, file) -> Map:
        file_bytes = await file.read()
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        s3_url = await s3_storage.upload_file(file_bytes, unique_filename)
        
        map_data.pmtiles_url = s3_url
        return cast(Map, self.map_repository.create(map_data)) # type: ignore
