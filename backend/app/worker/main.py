from httpx import AsyncClient
from arq.connections import RedisSettings
import clickhouse_connect

from app.worker.tasks.api_to_clickhouse import sync_CH_data_from_api
from app.config import settings

REDIS_SETTINGS = RedisSettings(host=settings.redis_host, port=settings.redis_port)

CLICKHOUSE_SETTINGS = {
    "host": settings.ch_host,
    "port": settings.ch_port,
    "username": settings.ch_user,
    "password": settings.ch_password,
    "database": settings.lz_schema,
}


async def startup(ctx):
    clickhouse_client = clickhouse_connect.get_async_client(**CLICKHOUSE_SETTINGS)
    ctx["clickhouse_client"] = clickhouse_client
    ctx["network_client"] = AsyncClient()


async def shutdown(ctx):
    await ctx["network_client"].aclose()
    await ctx["clickhouse_client"].close()


class WorkerSettings:
    functions = [sync_CH_data_from_api]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS
