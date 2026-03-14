from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash


def get_connection(database_url: str) -> psycopg.Connection:
    return psycopg.connect(database_url, row_factory=dict_row)


def init_db(database_url: str) -> None:
    base_dir = Path(__file__).resolve().parent.parent
    schema_path = base_dir / "database" / "schema.sql"

    with get_connection(database_url) as conn:
        conn.autocommit = True
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()
            for statement in [s.strip() for s in schema_sql.split(";") if s.strip()]:
                conn.execute(statement)

        existing_admin = conn.execute(
            "SELECT id FROM usuarios WHERE email = %s", ("admin@estoque.local",)
        ).fetchone()

        if not existing_admin:
            conn.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo)
                VALUES (%s, %s, %s, 'admin', TRUE)
                """,
                (
                    "Administrador",
                    "admin@estoque.local",
                    generate_password_hash("admin123"),
                ),
            )
