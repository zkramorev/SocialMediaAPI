from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.users.router import router as router_users
from app.users_relationships.router_action import router as router_request
from app.users_relationships.router_status import router as router_status

app = FastAPI()
app.include_router(router_users)
app.include_router(router_request)
app.include_router(router_status)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
