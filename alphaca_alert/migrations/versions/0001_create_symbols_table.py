"""create symbols table

Revision ID: 0001
Revises:
Create Date: 2026-05-10
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "symbols",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("asset_class", sa.String(), nullable=False),
        sa.Column("exchange", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("tradable", sa.Boolean(), nullable=False),
        sa.Column("marginable", sa.Boolean(), nullable=False),
        sa.Column("maintenance_margin_requirement", sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column("margin_requirement_long", sa.String(), nullable=True),
        sa.Column("margin_requirement_short", sa.String(), nullable=True),
        sa.Column("shortable", sa.Boolean(), nullable=False),
        sa.Column("easy_to_borrow", sa.Boolean(), nullable=False),
        sa.Column("fractionable", sa.Boolean(), nullable=False),
        sa.Column("attributes", postgresql.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol"),
    )


def downgrade() -> None:
    op.drop_table("symbols")
