"""make pattern_day_trader and daytrade_count nullable

Alpaca stopped returning these fields on /v2/account, so the landing zone
must accept rows without them.

Revision ID: ac6c466aea55
Revises: ff24ae658a54
Create Date: 2026-10-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ac6c466aea55'
down_revision: Union[str, Sequence[str], None] = 'ff24ae658a54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE landing_zone.alpaca_account_snapshot "
        "MODIFY COLUMN pattern_day_trader Nullable(Bool), "
        "MODIFY COLUMN daytrade_count Nullable(Int32)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Fails if any NULLs have landed; backfill them before downgrading.
    op.execute(
        "ALTER TABLE landing_zone.alpaca_account_snapshot "
        "MODIFY COLUMN pattern_day_trader Bool, "
        "MODIFY COLUMN daytrade_count Int32"
    )
