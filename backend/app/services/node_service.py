from app.repository.node_repository import NodeRepository
from app.services.base_service import BaseService


class NodeService(BaseService):
    def __init__(self, node_repository: NodeRepository):
        self.node_repository = node_repository
        super().__init__(node_repository)
