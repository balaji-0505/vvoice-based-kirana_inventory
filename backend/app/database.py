import logging
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger(__name__)

# Attempt configured DATABASE_URL; fallback smoothly to SQLite if MySQL is unavailable
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    # Test connection
    with engine.connect() as conn:
        logger.info(f"Connected successfully to primary database: {settings.DATABASE_URL}")
except Exception as e:
    logger.warning(f"Could not connect to {settings.DATABASE_URL} ({e}). Falling back to local SQLite database.")
    FALLBACK_URL = "sqlite:///./kirana_inventory.db"
    engine = create_engine(FALLBACK_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_sqlite_schema() -> None:
    """Upgrade legacy SQLite databases created before newer product columns existed."""
    if "sqlite" not in str(engine.url):
        return

    with engine.begin() as conn:
        inspector = inspect(conn)
        if "products" not in inspector.get_table_names():
            return

        existing_columns = {col["name"] for col in inspector.get_columns("products")}
        for column_name in ("telugu_name", "hindi_name"):
            if column_name not in existing_columns:
                logger.warning(f"Adding missing SQLite column '{column_name}' to products table.")
                conn.execute(text(f'ALTER TABLE products ADD COLUMN "{column_name}" VARCHAR(255)'))


ensure_sqlite_schema()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
