import uuid

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.dependencies import (
    get_alpaca_access_token,
    get_current_user,
    get_arq_redis,
    ArqRedis,
)
from app.api.database import get_ch_db
from app.api.services.dashboard.data_sources import (
    AccountDataSource,
    PosititonsDataSource,
)
from app.api.schemas import (
    JobResponse,
    SyncResponse,
    AccountOverviewOut,
    HoldingsOut,
    HoldingOut,
)
from app.api.models import AlpacaAccountSnapshot, AlpacaPositionSnapshot

router = APIRouter(prefix="/dashboard")


@router.post("/sync")
async def sync_dashboard(
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


@router.get("/account_overview")
def get_account_overview(
    user_id: uuid.UUID = Depends(get_current_user), ch_db: Session = Depends(get_ch_db)
) -> AccountOverviewOut:
    stmt = (
        select(AlpacaAccountSnapshot)
        .where(AlpacaAccountSnapshot.user_id == user_id)
        .order_by(AlpacaAccountSnapshot.batched_at.desc())
        .limit(1)
    )
    data = ch_db.scalars(stmt).first()
    if data is None:
        raise HTTPException(
            404, "Data is not available yet. Please sync the data first"
        )

    return AccountOverviewOut.model_validate(obj=data)


@router.get("/holdings")
def get_holdings(
    user_id: uuid.UUID = Depends(get_current_user),
    ch_db: Session = Depends(get_ch_db),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> HoldingsOut:
    latest_batched_at = (
        select(func.max(AlpacaPositionSnapshot.batched_at))
        .where(AlpacaPositionSnapshot.user_id == user_id)
        .scalar_subquery()
    )
    stmt = (
        select(AlpacaPositionSnapshot)
        .where(
            AlpacaPositionSnapshot.user_id == user_id,
            AlpacaPositionSnapshot.batched_at == latest_batched_at,
        )
        .order_by(
            AlpacaPositionSnapshot.market_value.desc(), AlpacaPositionSnapshot.symbol
        )
        .offset(offset)
        .limit(limit)
    )
    total_stmt = (
        select(func.count())
        .select_from(AlpacaPositionSnapshot)
        .where(
            AlpacaPositionSnapshot.user_id == user_id,
            AlpacaPositionSnapshot.batched_at == latest_batched_at,
        )
    )
    all_holdings = ch_db.scalars(stmt).all()
    holdings_cnt = ch_db.scalars(total_stmt).one()
    return HoldingsOut(
        holdings=all_holdings,
        total=holdings_cnt,
        batched_at=all_holdings[0].batched_at if all_holdings else None,
    )

# TODO: Onboarding the order ingestion into clickhouse and then will build a dedup on the fly to get the data
# TODO: In the future, we introduce a cronjob to dedup the data and to build a data mart
# @router.get("/orders")
# def get_orders():
#     pass