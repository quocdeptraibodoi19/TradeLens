import json
import uuid
from typing import Type, Any, Iterable
from datetime import datetime, UTC

import pyarrow as pa
from sqlalchemy import inspect
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from clickhouse_connect.cc_sqlalchemy.datatypes.sqltypes import (
    UUID as ChUUID,
    String as ChString,
    Bool as ChBool,
    Int32 as ChInt32,
    Decimal as ChDecimal,
    DateTime64 as ChDateTime64,
    Date as ChDate,
)
from httpx import AsyncClient
from clickhouse_connect.driver.asyncclient import AsyncClient as CHAsyncClient

from app.api.models import ClickhouseBase


async def stream_records(client: AsyncClient, url: str, token: str, user_id: str):
    batched_at = datetime.now(tz=UTC)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }
    async with client.stream("GET", url=url, headers=headers) as stream_response:
        stream_response.raise_for_status()
        for line in stream_response.aiter_lines():
            if line:
                json_data = json.loads(line)
                json_data["user_id"] = user_id
                json_data["batched_at"] = batched_at
                yield json_data


async def stream_batches(
    schema: pa.schema, records, batch_size=5000
) -> pa.record_batch:
    batches = []
    async for record in records:
        batches.append(record)

        if len(batches) >= batch_size:
            yield pa.RecordBatch.from_pylist(batches, schema=schema)
            batches.clear()

    if batches:
        yield pa.RecordBatch.from_pylist(batches, schema=schema)


def sqlalchemy_to_pyschema(columns: ReadOnlyColumnCollection) -> pa.schema:
    fields = []
    for column in columns:
        arrow_type = _sqlalchemy_type_to_arrow(column.type)

        fields.append(pa.field(column.name, arrow_type, nullable=column.nullable))

    return pa.schema(fields)


def _sqlalchemy_type_to_arrow(type_: Any) -> pa.DataType:
    if isinstance(type_, ChUUID):
        return pa.string()

    if isinstance(type_, ChString):
        return pa.string()

    if isinstance(type_, ChBool):
        return pa.bool_()

    if isinstance(type_, ChInt32):
        return pa.int32()

    if isinstance(type_, ChDateTime64):
        return pa.timestamp("us", tz="UTC" if type_.timezone else None)

    if isinstance(type_, ChDate):
        return pa.date64()

    if isinstance(type_, ChDecimal):
        return pa.decimal128()


async def ingest_data_to_CH(
    table_name: str, client: CHAsyncClient, record_batches: Iterable[pa.RecordBatch]
):
    async for batch in record_batches:
        client.insert(table=table_name, data=batch)


async def sync_CH_data_from_api(
    ctx,
    user_id: uuid.UUID,
    model_cls: Type[ClickhouseBase],
    api_url: str,
    token: str,
):
    client: AsyncClient = ctx["network_client"]
    clickhouse_client: CHAsyncClient = ctx["clickhouse_client"]
    table_name = model_cls.__tablename__
    schema = sqlalchemy_to_pyschema(columns=inspect(model_cls).columns)

    ingest_data_to_CH(
        table_name=table_name,
        client=clickhouse_client,
        record_batches=stream_batches(
            schema=schema,
            records=stream_records(
                client=client, url=api_url, token=token, user_id=user_id
            ),
        ),
    )
