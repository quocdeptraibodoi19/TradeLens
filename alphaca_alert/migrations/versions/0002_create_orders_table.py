"""create orders table

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-10
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("client_order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("asset_class", sa.String(), nullable=False),
        sa.Column("side", sa.String(), nullable=False),
        sa.Column("order_type", sa.String(), nullable=False),
        sa.Column("time_in_force", sa.String(), nullable=False),
        sa.Column("extended_hours", sa.Boolean(), nullable=False),
        sa.Column("qty", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("notional", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("limit_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("stop_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("trail_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("trail_percent", sa.Numeric(precision=8, scale=4), nullable=True),
        sa.Column("filled_qty", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("filled_avg_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("filled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("canceled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expired_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("replaces", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["symbol"], ["symbols.symbol"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("orders")
