import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from httpx import AsyncClient

from app.dependencies import (
    get_alpaca_access_token,
    get_current_user,
    get_arq_redis,
    get_http_client,
    ArqRedis,
)
from app.api.services.dashboard.alpaca_live import cache_key, fetch_alpaca, get_or_fetch
from app.api.services.dashboard.data_sources import (
    AccountDataSource,
    PosititonsDataSource,
)
from app.api.schemas import (
    JobResponse,
    SyncResponse,
    AccountOverviewOut,
    HoldingsOut,
)

router = APIRouter(prefix="/dashboard")


@router.post("/sync_analytics")
async def sync_analytics(
    user_id: uuid.UUID = Depends(get_current_user),
    alpaca_token: str = Depends(get_alpaca_access_token),
    arq_redis: ArqRedis = Depends(get_arq_redis),
) -> SyncResponse:

    jobs = []
    for source_cls in [AccountDataSource, PosititonsDataSource]:
        job = await arq_redis.enqueue_job(
            "sync_CH_data_from_api", user_id, source_cls, alpaca_token
        )

        jobs.append(JobResponse(job_id=job.job_id, url=source_cls.url))

    return SyncResponse(jobs=jobs)


@router.post("/sync")
async def sync_dashboard(
    user_id: uuid.UUID = Depends(get_current_user),
    redis: ArqRedis = Depends(get_arq_redis),
):
    await redis.delete(
        cache_key("account", user_id),
        cache_key("positions", user_id),
    )
    return {"refreshed": True}


@router.get("/account_overview")
async def get_account_overview(
    user_id: uuid.UUID = Depends(get_current_user),
    alpaca_token: str = Depends(get_alpaca_access_token),
    redis: ArqRedis = Depends(get_arq_redis),
    http_client: AsyncClient = Depends(get_http_client),
) -> AccountOverviewOut:
    account, fetched_at = await get_or_fetch(
        redis,
        cache_key("account", user_id),
        lambda: fetch_alpaca(http_client, AccountDataSource.url, alpaca_token),
    )
    return AccountOverviewOut.model_validate({**account, "batched_at": fetched_at})


@router.get("/holdings")
async def get_holdings(
    user_id: uuid.UUID = Depends(get_current_user),
    alpaca_token: str = Depends(get_alpaca_access_token),
    redis: ArqRedis = Depends(get_arq_redis),
    http_client: AsyncClient = Depends(get_http_client),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> HoldingsOut:
    positions, fetched_at = await get_or_fetch(
        redis,
        cache_key("positions", user_id),
        lambda: fetch_alpaca(http_client, PosititonsDataSource.url, alpaca_token),
    )
    # Positions are bounded by portfolio size, so sorting and paging in memory is fine
    ranked = sorted(
        positions,
        key=lambda p: (-Decimal(p.get("market_value") or 0), p["symbol"]),
    )
    return HoldingsOut(
        holdings=ranked[offset : offset + limit],
        total=len(ranked),
        batched_at=fetched_at,
    )


# TODO: Onboarding the order ingestion into clickhouse and then will build a dedup on the fly to get the data
# TODO: In the future, we introduce a cronjob to dedup the data and to build a data mart
# @router.get("/orders")
# def get_orders():
#     pass
