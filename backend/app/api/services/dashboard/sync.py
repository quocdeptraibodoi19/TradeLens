from typing import Type
from sqlalchemy import text, create_engine, inspect
from sqlalchemy.orm import Session

from app.config import settings
from app.api.models import AlpacaAccountSnapshot, AlpacaPositionSnapshot, ClickhouseBase

class ClickhouseSyncer:
    def __init__(self):
        self.clickhouse_engine = create_engine(settings.clickhouse_url)

    # We can use the Alembic to do this also. But I dont like it so doing it here for the sake of learning.
    # def sync_metadata(self, model_cls: Type[ClickhouseBase]):
    #     insp = inspect(self.clickhouse_engine)
    #     schema =  model_cls.__table__.schema
    #     table_name = model_cls.__tablename__

    #     if not insp.has_table(table_name, schema=schema):
    #         model_cls.__table__.create(self.clickhouse_engine)
    #         return

    #     existing_cols = {
    #         col["name"] for col in insp.get_columns(table_name, schema=schema)
    #     }
    #     model_cols = {c.name: c for c in model_cls.__table__.columns}
    #     missing = model_cols.keys() - existing_cols
    #     redundant = existing_cols - model_cols.keys()

    #     with self.clickhouse_engine.connect() as conn:
    #         for name in missing:
    #             ddl_type = model_cols[name].type.compile(dialect=self.clickhouse_engine.dialect)
    #             conn.execute(text(
    #                 f"ALTER TABLE {schema}.{table_name} "
    #                 f"ADD COLUMN IF NOT EXISTS {name} {ddl_type}"
    #             ))
            
    #         for name in redundant:
    #             conn.execute(text(
    #                 f"ALTER TABLE {schema}.{table_name} "
    #                 f"DROP COLUMN IF EXISTS {name}"
    #             ))
            
    #         conn.commit()


    def sync_data(self):
        pass

