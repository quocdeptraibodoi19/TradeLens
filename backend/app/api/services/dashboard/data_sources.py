from typing import Type, AsyncIterator, Callable
from enum import StrEnum

from httpx import AsyncClient
import ijson

from app.api.models import ClickhouseBase, AlpacaAccountSnapshot, AlpacaPositionSnapshot
from app.api.schemas import AlpacaPositionPayload, AlpacaAccountPayload, AlpacaPayload

Reader = Callable[[AsyncClient, str, dict], AsyncIterator[dict]]


class Shape(StrEnum):
    OBJECT = "object"
    ARRAY = "array"
    JSONL = "jsonl"


async def read_object(
    client: AsyncClient, url: str, headers: dict
) -> AsyncIterator[dict]:
    resp = await client.get(url=url, headers=headers)
    resp.raise_for_status()
    yield resp.json()


async def read_array(
    client: AsyncClient, url: str, headers: dict
) -> AsyncIterator[dict]:
    async with client.stream("GET", url=url, headers=headers) as resp:
        resp.raise_for_status()
        async for record in ijson.items(ijson.from_iter(resp.aiter_bytes()), "item"):
            yield record


async def read_jsonl(
    client: AsyncClient, url: str, headers: dict
) -> AsyncIterator[dict]:
    raise NotImplementedError("jsonl not supported yet")
    yield


READERS = {Shape.OBJECT: read_object, Shape.ARRAY: read_array, Shape.JSONL: read_jsonl}


class DataSource:
    model: Type[ClickhouseBase]
    validation: Type[AlpacaPayload]
    url: str
    shape: Shape

    @classmethod
    def get_reader(cls) -> Reader:
        return READERS[cls.shape]


class AccountDataSource(DataSource):
    model = AlpacaAccountSnapshot
    validation = AlpacaAccountPayload
    url = "https://paper-api.alpaca.markets/v2/account"
    shape: Shape = Shape.OBJECT


class PosititonsDataSource(DataSource):
    model = AlpacaPositionSnapshot
    validation = AlpacaPositionPayload
    url = "https://paper-api.alpaca.markets/v2/positions"
    shape: Shape = Shape.ARRAY
