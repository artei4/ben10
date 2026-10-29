"""Migra os usuários do SQLite local para o Supabase sem expor hashes.

Execute localmente na raiz do projeto, com SUPABASE_URL e
SUPABASE_SERVICE_ROLE_KEY definidos no ambiente. Não publique essas variáveis.
"""
import os
import sqlite3
from pathlib import Path

from supabase import create_client

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "omnitrix.db"


def main():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise SystemExit(
            "Defina SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY no ambiente antes de executar."
        )
    if not DB_PATH.exists():
        raise SystemExit(f"Banco SQLite não encontrado em: {DB_PATH}")

    sqlite_conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    sqlite_conn.row_factory = sqlite3.Row
    try:
        users = sqlite_conn.execute(
            "SELECT username, password FROM users ORDER BY id"
        ).fetchall()
    finally:
        sqlite_conn.close()

    client = create_client(url, key)
    inserted = 0
    already_present = 0

    for user in users:
        username = user["username"]
        password_hash = user["password"]

        existing = (
            client.table("app_users")
            .select("id")
            .eq("username", username)
            .limit(1)
            .execute()
        )
        if existing.data:
            already_present += 1
            continue

        (
            client.table("app_users")
            .insert({
                "username": username,
                "password_hash": password_hash,
            })
            .execute()
        )
        inserted += 1

    print("Migração concluída.")
    print(f"Contas encontradas no SQLite: {len(users)}")
    print(f"Contas novas transferidas: {inserted}")
    print(f"Contas já existentes no Supabase, preservadas: {already_present}")


if __name__ == "__main__":
    main()
