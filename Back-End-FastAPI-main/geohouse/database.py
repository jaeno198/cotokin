from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
 
 
# ──────────────────────────────────────────────
# Engine SQLite
# ──────────────────────────────────────────────
 
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # obrigatório para SQLite + FastAPI
    echo=settings.debug,                         # loga SQL no terminal se DEBUG=True
)
 
 
# ──────────────────────────────────────────────
# Habilita chaves estrangeiras no SQLite
# (desativadas por padrão no SQLite)
# ──────────────────────────────────────────────
 
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
 
 
# ──────────────────────────────────────────────
# Session factory
# ──────────────────────────────────────────────
 
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
 
 
# ──────────────────────────────────────────────
# Base declarativa compartilhada pelos models
# ──────────────────────────────────────────────
 
class Base(DeclarativeBase):
    pass
 
 
# ──────────────────────────────────────────────
# Dependency FastAPI — get_db
# ──────────────────────────────────────────────
 
def get_db():
    """
    Dependency injetada nos endpoints via Depends(get_db).
    Garante que a sessão é fechada após cada request,
    mesmo em caso de exceção.
 
    Uso nos routers:
        from database import get_db
        def meu_endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
# ──────────────────────────────────────────────
# Criação das tabelas (chamado no startup do main.py)
# ──────────────────────────────────────────────
 
def create_tables():
    """
    Cria todas as tabelas definidas nos models caso não existam.
    Chamado automaticamente no evento de startup do FastAPI.
    """
    import models  # noqa: F401 — garante que os models são registrados na Base
    Base.metadata.create_all(bind=engine)