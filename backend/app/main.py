from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container
from app.util.class_object import singleton


@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        self.container = Container()
        self.db = self.container.db()

        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        @self.app.get("/")
        def root():
            return "service is working"

        @self.app.get("/health")
        def health():
            try:
                with self.db.session() as session:
                    session.execute("SELECT 1")
                return {
                    "status": "ok",
                    "service": configs.PROJECT_NAME,
                    "database": "connected",
                    "version": "0.0.1"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "service": configs.PROJECT_NAME,
                    "database": "disconnected",
                    "error": str(e)
                }

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container
