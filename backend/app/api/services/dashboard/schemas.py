import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class AlpacaUserAccountSnapshotSchema(BaseModel):
    # identifiers & status
    account_number: str
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


class AlpacaUserPositionSnapshotSchema(BaseModel):
    # identifiers
    asset_id: uuid.UUID
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
