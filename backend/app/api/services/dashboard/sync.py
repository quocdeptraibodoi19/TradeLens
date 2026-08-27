import uuid
from typing import Type, Union, List
from datetime import datetime, UTC

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings
from app.api.models import ClickhouseBase


class ClickhouseSyncer:
    def __init__(self):
        self.clickhouse_engine = create_engine(settings.clickhouse_url)

    def sync_data(
        self,
        user_id: uuid.UUID,
        model_cls: Type[ClickhouseBase],
        response_data: Union[BaseModel, List[BaseModel]],
    ):
        """
        Append-only sycing data.
        """
        batched_at = datetime.now(tz=UTC)
        if not isinstance(response_data, list):
            response_data = [response_data]
        records = [
            model_cls(**{**data.model_dump(), "user_id": user_id, "batched_at": batched_at})
            for data in response_data
        ]

        with Session(self.clickhouse_engine) as session:
            session.bulk_save_objects(records)
            session.commit()


clichouse_syncer = ClickhouseSyncer()

def get_clickhouse_syncer():
    return clichouse_syncer
