import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, LargeBinary, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    access_token_enc = Column(LargeBinary, nullable=False)
    token_type = Column(String, default="bearer")
    scope = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class AlpacaAccInfo(Base):
    __tablename__ = "alpaca_acc_infos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    account_number = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    cash = Column(String, nullable=False)
    portfolio_value = Column(String, nullable=False)
    equity = Column(String, nullable=False)
    last_equity = Column(String, nullable=False)
    long_market_value = Column(String, nullable=False)
    short_market_value = Column(String, nullable=False)
    position_market_value = Column(String, nullable=False)
    buying_power = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

