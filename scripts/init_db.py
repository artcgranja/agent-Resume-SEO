#!/usr/bin/env python3
"""
Script para inicializar/sincronizar o banco de dados PostgreSQL
Ações: check | init | reset | sync
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import create_tables, drop_tables, engine
from sqlalchemy.orm import Session
from sqlalchemy import text

def init_database():
    """Cria todas as tabelas se não existirem."""
    print("Inicializando banco de dados...")
    create_tables()
    # Verificar tabelas criadas
    with Session(engine) as session:
        result = session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
        tables = ", ".join(row[0] for row in result)
        print(f"Tabelas: {tables}" if tables else "Nenhuma tabela encontrada.")
    print("OK")

def reset_database():
    """Remove e recria todas as tabelas."""
    print("Resetando banco de dados...")
    drop_tables()
    create_tables()
    print("OK")

def check_connection():
    """Verifica a conexão com o banco de dados."""
    print("Checando conexão...")
    with Session(engine) as session:
        version = session.execute(text("SELECT version()"))
        print(f"Conectado: {version.fetchone()[0]}")
    print("OK")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerenciamento do banco de dados")
    parser.add_argument("action", choices=["init", "reset", "check", "sync"], help="Ação a executar")
    args = parser.parse_args()

    if args.action in ("init", "sync"):
        init_database()
    elif args.action == "reset":
        reset_database()
    elif args.action == "check":
        check_connection()
