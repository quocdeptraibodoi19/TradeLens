import uuid
from datetime import datetime, timezone
from typing import TypeVar

from sqlalchemy import (
    Column,
    String,
    LargeBinary,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    MetaData,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import DeclarativeBase
from clickhouse_connect.cc_sqlalchemy.ddl.tableengine import MergeTree
from clickhouse_connect.cc_sqlalchemy.datatypes.sqltypes import (
    UUID as ChUUID,
    String as ChString,
    Bool as ChBool,
    Int32 as ChInt32,
    Decimal as ChDecimal,
    DateTime64 as ChDateTime64,
    Date as ChDate,
    Nullable as ChNullable,
)

from app.config import settings


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))


class UserAlpacaToken(Base):
    __tablename__ = "user_alpaca_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    access_token_enc = Column(LargeBinary, nullable=False)
    token_type = Column(String, default="bearer")
    scope = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))


class ClickhouseBase(DeclarativeBase):
    metadata = MetaData(schema=settings.lz_schema)


class AlpacaAccountSnapshot(ClickhouseBase):
    __tablename__ = "alpaca_account_snapshot"
    __table_args__ = (MergeTree(order_by=["user_id", "batched_at"]),)

    # from AlpacaSnapshot
    user_id = Column(ChUUID, primary_key=True, nullable=False)
    batched_at = Column(ChDateTime64(3, tz="UTC"), primary_key=True, nullable=False)

    # identifiers & status
    account_number = Column(ChString, nullable=False)
    status = Column(ChString, nullable=False)
    crypto_status = Column(ChNullable(ChString))
    currency = Column(ChString, nullable=False)

    # options
    options_approved_level = Column(ChNullable(ChInt32))
    options_trading_level = Column(ChNullable(ChInt32))

    # buying power
    buying_power = Column(ChDecimal(38, 10), nullable=False)
    regt_buying_power = Column(ChNullable(ChDecimal(38, 10)))
    daytrading_buying_power = Column(ChNullable(ChDecimal(38, 10)))
    effective_buying_power = Column(ChNullable(ChDecimal(38, 10)))
    non_marginable_buying_power = Column(ChNullable(ChDecimal(38, 10)))
    options_buying_power = Column(ChNullable(ChDecimal(38, 10)))
    bod_dtbp = Column(ChNullable(ChDecimal(38, 10)))

    # cash & fees
    cash = Column(ChDecimal(38, 10), nullable=False)
    accrued_fees = Column(ChNullable(ChDecimal(38, 10)))
    pending_reg_taf_fees = Column(ChNullable(ChDecimal(38, 10)))
    intraday_adjustments = Column(ChNullable(ChDecimal(38, 10)))

    # portfolio values
    portfolio_value = Column(ChDecimal(38, 10), nullable=False)
    equity = Column(ChDecimal(38, 10), nullable=False)
    last_equity = Column(ChNullable(ChDecimal(38, 10)))
    long_market_value = Column(ChNullable(ChDecimal(38, 10)))
    short_market_value = Column(ChNullable(ChDecimal(38, 10)))
    position_market_value = Column(ChNullable(ChDecimal(38, 10)))

    # margin
    initial_margin = Column(ChNullable(ChDecimal(38, 10)))
    maintenance_margin = Column(ChNullable(ChDecimal(38, 10)))
    last_maintenance_margin = Column(ChNullable(ChDecimal(38, 10)))
    sma = Column(ChNullable(ChDecimal(38, 10)))

    # flags
    pattern_day_trader = Column(ChBool, nullable=False)
    trading_blocked = Column(ChBool, nullable=False)
    transfers_blocked = Column(ChBool, nullable=False)
    account_blocked = Column(ChBool, nullable=False)
    trade_suspended_by_user = Column(ChBool, nullable=False)
    shorting_enabled = Column(ChBool, nullable=False)

    # misc
    multiplier = Column(ChNullable(ChString))
    daytrade_count = Column(ChInt32, nullable=False)
    balance_asof = Column(ChNullable(ChDate))
    crypto_tier = Column(ChNullable(ChInt32))


class AlpacaPositionSnapshot(ClickhouseBase):
    __tablename__ = "alpaca_position_snapshot"
    __table_args__ = (MergeTree(order_by=["user_id", "asset_id"]),)

    # from AlpacaSnapshot
    user_id = Column(ChUUID, primary_key=True, nullable=False)
    batched_at = Column(ChDateTime64(3, tz="UTC"), primary_key=True, nullable=False)

    # identifiers
    asset_id = Column(ChUUID, primary_key=True, nullable=False)
    symbol = Column(ChString, nullable=False)
    exchange = Column(ChString, nullable=False)
    asset_class = Column(ChString, nullable=False)
    asset_marginable = Column(ChNullable(ChBool))
    side = Column(ChString, nullable=False)

    # position size
    qty = Column(ChDecimal(38, 10), nullable=False)
    qty_available = Column(ChDecimal(38, 10), nullable=False)

    # pricing
    avg_entry_price = Column(ChDecimal(38, 10), nullable=False)
    current_price = Column(ChNullable(ChDecimal(38, 10)))
    lastday_price = Column(ChNullable(ChDecimal(38, 10)))
    change_today = Column(ChNullable(ChDecimal(38, 10)))

    # value & P&L
    market_value = Column(ChNullable(ChDecimal(38, 10)))
    cost_basis = Column(ChNullable(ChDecimal(38, 10)))
    unrealized_pl = Column(ChNullable(ChDecimal(38, 10)))
    unrealized_plpc = Column(ChNullable(ChDecimal(38, 10)))
    unrealized_intraday_pl = Column(ChNullable(ChDecimal(38, 10)))
    unrealized_intraday_plpc = Column(ChNullable(ChDecimal(38, 10)))
