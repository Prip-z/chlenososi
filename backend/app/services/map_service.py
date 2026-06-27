from app.repository.map_repository import MapRepository
from app.services.base_service import BaseService
from app.schema.map_schema import BoundingBox, Map, MapAreaResponse
from app.core.exceptions import NotFoundError
import uuid
from app.core.s3 import s3_storage
from app.schema.map_schema import UpsertMap

from app.schema.map_schema import NodeResponse, EdgeResponse, MapAreaResponse, BoundingBox
from app.core.exceptions import NotFoundError 

from app.util.geojson import to_geojson

from typing import cast

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
        import uuid
        from typing import Any, cast
        
        # 1. Генерируем уникальное имя файла для S3
        file_extension = file.filename.split('.')[-1] if file.filename else 'pmtiles'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # 2. Загружаем файл в MinIO S3 (передаем file.file, чтобы boto3 не ругался)
        s3_url = await s3_storage.upload_file(file.file, unique_filename)
        
        # 3. Прописываем полученный URL в схему данных
        map_data.pmtiles_url = s3_url
        
        # 4. Передаем схему в репозиторий, применив cast к Any, чтобы линтер пропустил тип
        # Репозиторий внутри себя вызовет map_data.dict() и создаст модель БД
        created_db_model = self.map_repository.create(cast(Any, map_data))
        
        # 5. Возвращаем схему ответа
        from app.schema.map_schema import Map as SchemaMap
        return cast(SchemaMap, created_db_model)
    
    def get_map_as_geojson(self, map_id: int, bbox: BoundingBox):
        
        nodes_data = self.map_repository.get_nodes_in_bbox(
            map_id, bbox.min_lon, bbox.min_lat, bbox.max_lon, bbox.max_lat
        )
        node_ids = [n['id'] for n in nodes_data]
        edges_data = self.map_repository.get_edges_by_node_ids(map_id, node_ids)
        
        return to_geojson(nodes_data, edges_data)  

 