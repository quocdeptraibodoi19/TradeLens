import json
import uuid
from datetime import datetime, UTC
from typing import Any, Awaitable, Callable

from arq.connections import ArqRedis
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, HTTPError, HTTPStatusError

CACHE_TTL_SECONDS = 30


def cache_key(name: str, user_id: uuid.UUID) -> str:
    # Must include user_id, otherwise one user's portfolio is served to another
    return f"tradelens:{name}:{user_id}"


async def fetch_alpaca(client: AsyncClient, url: str, token: str) -> Any:
    try:
        resp = await client.get(
            url,
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {token}",
            },
        )
        resp.raise_for_status()
    except HTTPStatusError as e:
        if e.response.status_code in (401, 403):
            raise HTTPException(502, "Alpaca rejected the token. Reconnect your Alpaca account.")
        raise HTTPException(502, f"Alpaca returned {e.response.status_code}")
    except HTTPError:
        raise HTTPException(502, "Could not reach Alpaca")
    return resp.json()


async def get_or_fetch(
    redis: ArqRedis,
    key: str,
    fetch: Callable[[], Awaitable[Any]],
    ttl: int = CACHE_TTL_SECONDS,
) -> tuple[Any, datetime]:
    """Cache-aside read. Returns (data, fetched_at)."""
    if (cached := await redis.get(key)) is not None:
        entry = json.loads(cached)
        return entry["data"], datetime.fromisoformat(entry["fetched_at"])

    data = await fetch()
    fetched_at = datetime.now(tz=UTC)
    await redis.set(
        key,
        json.dumps({"data": data, "fetched_at": fetched_at.isoformat()}),
        ex=ttl,
    )
    return data, fetched_at
