from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = (
    f"postgresql://{settings.app_db_user}:{settings.app_db_password}"
    f"@{settings.app_db_host}:{settings.app_db_port}"
    f"/{settings.app_db_name}"
)

engine = create_engine(url=DATABASE_URL)

def get_db():
    db = sessionmaker(bind=engine, autoflush=False)()
    try:
        yield db
    finally:
        db.close()
