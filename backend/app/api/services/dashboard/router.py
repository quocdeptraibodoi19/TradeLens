import uuid

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
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
from app.api.schemas import JobResponse, SyncResponse, AccountOverviewOut
from app.api.models import AlpacaAccountSnapshot

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
