import uuid

import httpx
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies import get_alpaca_access_token, get_current_user
from app.api.services.dashboard.schemas import (
    AlpacaUserAccountSnapshotSchema,
    AlpacaUserPositionSnapshotSchema,
)
from app.api.models import AlpacaAccountSnapshot, AlpacaPositionSnapshot
from app.api.services.dashboard.sync import get_clickhouse_syncer, ClickhouseSyncer

router = APIRouter(prefix="/dashboard")


@router.post("/sync")
async def sync_dashboard(
    user_id: uuid.UUID = Depends(get_current_user),
    alpaca_token: str = Depends(get_alpaca_access_token),
    clickhouse_syncer: ClickhouseSyncer = Depends(get_clickhouse_syncer),
):
    base_url = "https://paper-api.alpaca.markets/v2"
    async with httpx.AsyncClient() as client:
        # Get user account
        account_response = await client.get(
            url=f"{base_url}/account",
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {alpaca_token}",
            },
        )
        positions_response = await client.get(
            url=f"{base_url}/positions",
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {alpaca_token}",
            },
        )

    account = AlpacaUserAccountSnapshotSchema(**account_response.json())
    positions = [
        AlpacaUserPositionSnapshotSchema(**position)
        for position in positions_response.json()
    ]

    clickhouse_syncer.sync_data(
        user_id=user_id, model_cls=AlpacaAccountSnapshot, response_data=account
    )
    clickhouse_syncer.sync_data(
        user_id=user_id, model_cls=AlpacaPositionSnapshot, response_data=positions
    )
