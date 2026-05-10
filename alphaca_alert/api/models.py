from sqlalchemy import Column, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Symbol(Base):
    __tablename__ = "symbols"

    id                           = Column("id", UUID(as_uuid=True), primary_key=True)
    symbol                       = Column("symbol", String, nullable=False, unique=True)
    name                         = Column("name", String, nullable=True)
    asset_class                  = Column("asset_class", String, nullable=False)
    exchange                     = Column("exchange", String, nullable=False)
    status                       = Column("status", String, nullable=False)
    tradable                     = Column("tradable", Boolean, nullable=False)
    marginable                   = Column("marginable", Boolean, nullable=False)
    maintenance_margin_requirement = Column("maintenance_margin_requirement", Numeric(8, 2), nullable=True)
    margin_requirement_long      = Column("margin_requirement_long", String, nullable=True)
    margin_requirement_short     = Column("margin_requirement_short", String, nullable=True)
    shortable                    = Column("shortable", Boolean, nullable=False)
    easy_to_borrow               = Column("easy_to_borrow", Boolean, nullable=False)
    fractionable                 = Column("fractionable", Boolean, nullable=False)
    attributes                   = Column("attributes", ARRAY(String), nullable=True, default=list)


class Order(Base):
    __tablename__ = "orders"

    id                = Column("id", UUID(as_uuid=True), primary_key=True)
    client_order_id   = Column("client_order_id", UUID(as_uuid=True), nullable=False)
    asset_id          = Column("asset_id", UUID(as_uuid=True), nullable=False)

    symbol            = Column("symbol", String, ForeignKey("symbols.symbol"), nullable=False)
    asset_class       = Column("asset_class", String, nullable=False)
    side              = Column("side", String, nullable=False)
    order_type        = Column("order_type", String, nullable=False)
    time_in_force     = Column("time_in_force", String, nullable=False)
    extended_hours    = Column("extended_hours", Boolean, nullable=False, default=False)

    qty               = Column("qty", Numeric(12, 4), nullable=True)
    notional          = Column("notional", Numeric(12, 4), nullable=True)

    limit_price       = Column("limit_price", Numeric(12, 4), nullable=True)
    stop_price        = Column("stop_price", Numeric(12, 4), nullable=True)
    trail_price       = Column("trail_price", Numeric(12, 4), nullable=True)
    trail_percent     = Column("trail_percent", Numeric(8, 4), nullable=True)

    filled_qty        = Column("filled_qty", Numeric(12, 4), nullable=False, default=0)
    filled_avg_price  = Column("filled_avg_price", Numeric(12, 4), nullable=True)

    status            = Column("status", String, nullable=False)

    created_at        = Column("created_at", DateTime(timezone=True), nullable=False)
    updated_at        = Column("updated_at", DateTime(timezone=True), nullable=False)
    submitted_at      = Column("submitted_at", DateTime(timezone=True), nullable=True)
    filled_at         = Column("filled_at", DateTime(timezone=True), nullable=True)
    canceled_at       = Column("canceled_at", DateTime(timezone=True), nullable=True)
    expired_at        = Column("expired_at", DateTime(timezone=True), nullable=True)
    failed_at         = Column("failed_at", DateTime(timezone=True), nullable=True)
    replaced_at       = Column("replaced_at", DateTime(timezone=True), nullable=True)
    replaced_by       = Column("replaced_by", UUID(as_uuid=True), nullable=True)
    replaces          = Column("replaces", UUID(as_uuid=True), nullable=True)
    expires_at        = Column("expires_at", DateTime(timezone=True), nullable=True)


class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id           = Column("id", UUID(as_uuid=True), primary_key=True)
    symbol       = Column("symbol", String, ForeignKey("symbols.symbol"), nullable=False)
    condition    = Column("condition", String, nullable=False)
    threshold    = Column("threshold", Numeric(12, 4), nullable=False)
    status       = Column("status", String, nullable=False, default="active")
    created_at   = Column("created_at", DateTime(timezone=True), nullable=False)
    triggered_at = Column("triggered_at", DateTime(timezone=True), nullable=True)
