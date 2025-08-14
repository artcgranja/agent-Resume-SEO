import os
from contextlib import contextmanager
from typing import Generator, Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.base import Base

# Configuração do PostgreSQL alinhada com docker-compose e agents.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://resume:resume@localhost:5452/resume_db",
)

# Configuração do engine (sem StaticPool para Postgres)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # Altere para True para depurar SQL
)

# Criação da sessão
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@contextmanager
def get_db() -> Iterator[Session]:
    """Context manager para obter sessão do banco de dados.
    Permite uso: `with get_db() as db:`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)

def drop_tables() -> None:
    """Remove todas as tabelas do banco de dados"""
    Base.metadata.drop_all(bind=engine)

__all__ = ["engine", "SessionLocal", "get_db", "create_tables", "drop_tables"]