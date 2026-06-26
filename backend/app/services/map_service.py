from app.repository.map_repository import MapRepository
from app.services.base_service import BaseService
from app.schema.map_schema import BoundingBox, MapAreaResponse
from app.core.exceptions import NotFoundError


class MapService(BaseService):
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository
        super().__init__(map_repository)

    def download_area(self, map_id: int, bbox: BoundingBox) -> MapAreaResponse:
        # 1. Получаем инфу о карте (ссылку на PMTiles)
        map_info = self.get_by_id(map_id)
        if not map_info:
            raise NotFoundError("Карта не найдена")

        # 2. Вытаскиваем все узлы в квадрате
        nodes_data = self.map_repository.get_nodes_in_bbox(
            map_id, bbox.min_lon, bbox.min_lat, bbox.max_lon, bbox.max_lat
        )

        # 3. Вытаскиваем ребра только для найденных узлов
        node_ids = [node['id'] for node in nodes_data]
        edges_data = []
        if node_ids:
            edges_data = self.map_repository.get_edges_by_node_ids(map_id, node_ids)

        return MapAreaResponse(
            map_id=map_info.id,
            pmtiles_url=map_info.pmtiles_url,
            nodes=nodes_data,
            edges=edges_data
        )