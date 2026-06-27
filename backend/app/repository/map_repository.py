from contextlib import AbstractContextManager
from typing import Callable, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.model.map_graph import Node, Edge, Map
from app.repository.base_repository import BaseRepository


class MapRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Map)  # Base будет работать с картами

    def get_nodes_in_bbox(self, map_id: int, min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> List[
        dict]:
        with self.session_factory() as session:
            bbox = func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)

            query = session.query(
                Node.id, Node.map_id, Node.is_walkable, Node.terrain_type,
                func.ST_Y(Node.geom).label('lat'),
                func.ST_X(Node.geom).label('lon')
            ).filter(
                Node.map_id == map_id,
                func.ST_Intersects(Node.geom, bbox)
            )

            return [row._asdict() for row in query.all()]

    def get_edges_by_node_ids(self, map_id: int, node_ids: List[int]) -> List[Edge]:
        with self.session_factory() as session:
            return session.query(Edge).filter(
                Edge.map_id == map_id,
                Edge.source_id.in_(node_ids) # type: ignore
            ).all()