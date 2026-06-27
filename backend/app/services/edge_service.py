from typing import Any
from app.repository.edge_repository import EdgeRepository
from app.services.base_service import BaseService
from app.schema.edge_schema import UpsertEdge

class EdgeService(BaseService):
    def __init__(self, edge_repository: EdgeRepository):
        self.edge_repository = edge_repository
        super().__init__(edge_repository)

    def add(self, edge_data: UpsertEdge) -> Any:
        data = edge_data.dict(exclude_none=True)
        data.pop("id", None)
        
        clean_edge = UpsertEdge(**data)
        
        return self.edge_repository.create(clean_edge) # type: ignore

    def remove_by_id(self, edge_id: int) -> Any:
        return self.edge_repository.delete_by_id(edge_id)