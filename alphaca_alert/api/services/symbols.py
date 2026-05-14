import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert


from api.models import Symbol

load_dotenv()


def sync_symbols(db: Session) -> int:
    client = TradingClient(
        os.environ["ALPACA_API_KEY"],
        os.environ["ALPACA_API_SECRET"],
        paper=True,
    )
    assets = client.get_all_assets(
        GetAssetsRequest(asset_class=AssetClass.US_EQUITY, status=AssetStatus.ACTIVE)
    )
    rows = [
        {
            "id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_class": asset.asset_class.value,
            "exchange": asset.exchange.value,
            "status": asset.status.value,
            "marginable": asset.marginable,
            "maintenance_margin_requirement": asset.maintenance_margin_requirement,
            "margin_requirement_long": asset.margin_requirement_long,
            "margin_requirement_short": asset.margin_requirement_short,
            "shortable": asset.shortable,
            "easy_to_borrow": asset.easy_to_borrow,
            "fractionable": asset.fractionable,
            "attributes": [a.value for a in asset.attributes],
        }
        for asset in assets
    ]
    stmt = insert(Symbol).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={col: stmt.excluded[col] for col in rows[0].keys() if col != 'id'}
    )
    db.execute(stmt)
    db.commit()

    return len(rows)
