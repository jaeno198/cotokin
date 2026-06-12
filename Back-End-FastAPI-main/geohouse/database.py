from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


# ── Engine MariaDB ────────────────────────────
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,      # verifica conexão antes de usar
    pool_recycle=3600,       # recicla conexões a cada 1h
    pool_size=5,
    max_overflow=10,
)


# ── Session factory ───────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ── Base declarativa ──────────────────────────
class Base(DeclarativeBase):
    pass


# ── Dependency FastAPI ────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Criação das tabelas ───────────────────────
def create_tables():
    import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
