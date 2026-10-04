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
from app.api.services.dashboard.data_sources import DataSource, Reader
from app.api.schemas import AlpacaPayload


async def stream_records(
    client: AsyncClient,
    url: str,
    token: str,
    user_id: uuid.UUID,
    data_reader: Reader,
    payload_cls: Type[AlpacaPayload],
):
    batched_at = datetime.now(tz=UTC)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }
    async for record in data_reader(client, url, headers):
        record["user_id"] = user_id
        record["batched_at"] = batched_at
        yield payload_cls(**record).model_dump()


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
        return pa.decimal128(type_.ch_type.prec, type_.ch_type.scale)


async def ingest_data_to_CH(
    database_name: str,
    table_name: str,
    client: CHAsyncClient,
    record_batches: Iterable[pa.RecordBatch],
):
    async for batch in record_batches:
        await client.insert_arrow(
            table=table_name,
            arrow_table=pa.Table.from_batches([batch]),
            database=database_name,
        )


async def sync_CH_data_from_api(
    ctx,
    user_id: uuid.UUID,
    source_cls: Type[DataSource],
    token: str,
):
    client: AsyncClient = ctx["network_client"]
    clickhouse_client: CHAsyncClient = ctx["clickhouse_client"]
    model_class = source_cls.model
    validation_class = source_cls.validation
    api_url = source_cls.url
    data_reader = source_cls.get_reader()
    table_name = model_class.__tablename__
    database_name = model_class.__table__.schema
    schema = sqlalchemy_to_pyschema(columns=inspect(model_class).columns)

    await ingest_data_to_CH(
        database_name=database_name,
        table_name=table_name,
        client=clickhouse_client,
        record_batches=stream_batches(
            schema=schema,
            records=stream_records(
                client=client,
                url=api_url,
                token=token,
                user_id=user_id,
                data_reader=data_reader,
                payload_cls=validation_class,
            ),
        ),
    )
