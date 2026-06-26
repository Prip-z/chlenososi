from app.repository.edge_repository import EdgeRepository
from app.services.base_service import BaseService


class EdgeService(BaseService):
    def __init__(self, edge_repository: EdgeRepository):
        self.edge_repository = edge_repository
        super().__init__(edge_repository)
