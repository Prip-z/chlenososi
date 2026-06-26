from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.map import router as map_router
from app.api.v1.endpoints.user import router as user_router

routers = APIRouter()
router_list = [auth_router, user_router, map_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
