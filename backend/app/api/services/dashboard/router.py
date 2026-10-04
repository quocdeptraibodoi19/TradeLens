import uuid

from fastapi import APIRouter, Depends


from app.dependencies import (
    get_alpaca_access_token,
    get_current_user,
    get_arq_redis,
    ArqRedis,
)
from app.api.services.dashboard.data_sources import AccountDataSource, PosititonsDataSource
from app.api.schemas import JobResponse, SyncResponse

router = APIRouter(prefix="/dashboard")


@router.post("/sync")
async def sync_dashboard(
    user_id: uuid.UUID = Depends(get_current_user),
    alpaca_token: str = Depends(get_alpaca_access_token),
    arq_redis: ArqRedis = Depends(get_arq_redis),
) -> SyncResponse:

    jobs = []
    for source_cls in [
        AccountDataSource,
        PosititonsDataSource
    ]:
        job = await arq_redis.enqueue_job(
            "sync_CH_data_from_api", user_id, source_cls, alpaca_token
        )

        jobs.append(JobResponse(job_id=job.job_id, url=source_cls.url))

    return SyncResponse(jobs=jobs)


# @router.get("/account_overview")
# async def get_account_overview(
#     user_id: uuid.UUID = Depends(get_current_user),
#     alpaca_token: str = Depends(get_alpaca_access_token),
#     clickhouse_syncer: ClickhouseSyncer = Depends(get_clickhouse_syncer),
# ):
#     pass
