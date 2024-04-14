from fastapi import APIRouter

from .endpoints import banners_router, user_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(
    banners_router,
    tags=['Управление баннерами']
)
main_router.include_router(user_router)
