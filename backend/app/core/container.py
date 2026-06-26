from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repository.map_repository import MapRepository
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.map_service import MapService
from app.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
            "app.api.v1.endpoints.map",
            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    map_repository = providers.Factory(MapRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    map_service = providers.Factory(MapService, map_repository=map_repository)