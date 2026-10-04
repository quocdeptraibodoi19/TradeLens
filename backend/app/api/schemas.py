from datetime import date
from decimal import Decimal
from uuid import UUID
from typing import Any, Annotated

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    AliasChoices,
    model_validator,
    Field,
    PlainSerializer
)


class JobResponse(BaseModel):
    job_id: str
    url: str


class SyncResponse(BaseModel):
    jobs: list[JobResponse]


UUIDStr = Annotated[UUID, PlainSerializer(str, return_type=str)]

class AlpacaPayload(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        coerce_numbers_to_str=True,
        str_strip_whitespace=True,
    )
    user_id: UUIDStr
    batched_at: AwareDatetime

    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                k: None if isinstance(v, str) and not v.strip() else v
                for k, v in data.items()
            }
        return data


class AlpacaAccountPayload(AlpacaPayload):
    # identifiers & status
    account_number: str = Field(validation_alias=AliasChoices("account_number", "id"))
    status: str
    crypto_status: str | None = None
    currency: str

    # options
    options_approved_level: int | None = None
    options_trading_level: int | None = None

    # buying power
    buying_power: Decimal
    regt_buying_power: Decimal | None = None
    daytrading_buying_power: Decimal | None = None
    effective_buying_power: Decimal | None = None
    non_marginable_buying_power: Decimal | None = None
    options_buying_power: Decimal | None = None
    bod_dtbp: Decimal | None = None

    # cash & fees
    cash: Decimal
    accrued_fees: Decimal | None = None
    pending_reg_taf_fees: Decimal | None = None
    intraday_adjustments: Decimal | None = None

    # portfolio values
    portfolio_value: Decimal
    equity: Decimal
    last_equity: Decimal | None = None
    long_market_value: Decimal | None = None
    short_market_value: Decimal | None = None
    position_market_value: Decimal | None = None

    # margin
    initial_margin: Decimal | None = None
    maintenance_margin: Decimal | None = None
    last_maintenance_margin: Decimal | None = None
    sma: Decimal | None = None

    # flags
    pattern_day_trader: bool
    trading_blocked: bool
    transfers_blocked: bool
    account_blocked: bool
    trade_suspended_by_user: bool
    shorting_enabled: bool

    # misc
    multiplier: str | None = None
    daytrade_count: int
    balance_asof: date | None = None
    crypto_tier: int | None = None


class AlpacaPositionPayload(AlpacaPayload):
    # identifiers
    asset_id: UUIDStr
    symbol: str
    exchange: str
    asset_class: str
    asset_marginable: bool | None = None
    side: str

    # position size
    qty: Decimal
    qty_available: Decimal

    # pricing
    avg_entry_price: Decimal
    current_price: Decimal | None = None
    lastday_price: Decimal | None = None
    change_today: Decimal | None = None

    # value & P&L
    market_value: Decimal | None = None
    cost_basis: Decimal | None = None
    unrealized_pl: Decimal | None = None
    unrealized_plpc: Decimal | None = None
    unrealized_intraday_pl: Decimal | None = None
    unrealized_intraday_plpc: Decimal | None = None
