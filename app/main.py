from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version
)

app.include_router(main_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_first_superuser()
