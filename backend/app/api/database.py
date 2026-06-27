from abc import ABC

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = {
    "postgres": f"postgresql://{settings.app_db_user}:{settings.app_db_password}"
    f"@{settings.app_db_host}:{settings.app_db_port}"
    f"/{settings.app_db_name}",
    "clickhouse": f"clickhouse+connect://{settings.ch_user}:{settings.ch_password}"
    f"@{settings.ch_host}:{settings.ch_port}/{settings.ch_database}",
}


postgres_engine = create_engine(url=DATABASE_URL["postgres"])
clickhouse_engine = create_engine(url=DATABASE_URL["clickhouse"])


def get_db(is_dw: bool = False):
    if is_dw:
        db = sessionmaker(bind=clickhouse_engine, autoflush=False)()
    else:
        db = sessionmaker(bind=postgres_engine, autoflush=False)()
    try:
        yield db
    finally:
        db.close()
