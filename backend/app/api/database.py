from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

url_mappings = {
    "postgres": settings.postgres_url,
    "clickhouse": settings.clickhouse_url,
}
engines = {name: create_engine(url) for name, url in url_mappings.items()}
session_factories = {name: sessionmaker(bind=e) for name, e in engines.items()}


def _session(name: str) -> Generator[Session, None, None]:
    db = session_factories[name]()
    try:
        yield db
    finally:
        db.close()


def get_db():
    yield from _session("postgres")


def get_ch_db():
    yield from _session("clickhouse")
