from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Convert the async URL (postgresql+asyncpg://) to a sync one (postgresql+psycopg2://)
SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://", "postgresql+psycopg2://"
)

engine = create_engine(
    SYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine)