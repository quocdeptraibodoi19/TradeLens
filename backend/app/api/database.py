import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('APP_DB_USER')}:{os.getenv('APP_DB_PASSWORD')}"
    f"@{os.getenv('APP_DB_HOST', 'localhost')}:{os.getenv('APP_DB_PORT', '5432')}"
    f"/{os.getenv('APP_DB_NAME')}"
)

engine = create_engine(url=DATABASE_URL)

def get_db():
    db = sessionmaker(bind=engine, autoflush=False)()
    try:
        yield db
    finally:
        db.close()
