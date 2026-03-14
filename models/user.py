from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from models.database import get_connection


class UserModel:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def authenticate(self, email: str, password: str) -> Optional[dict]:
        with get_connection(self.database_url) as conn:
            row = conn.execute(
                "SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE", (email,)
            ).fetchone()

        if row and check_password_hash(row["senha_hash"], password):
            return dict(row)
        return None

    def list_users(self) -> list[dict]:
        with get_connection(self.database_url) as conn:
            rows = conn.execute(
                "SELECT id, nome, email, perfil, ativo, data_criacao FROM usuarios ORDER BY id"
            ).fetchall()
        return [dict(row) for row in rows]

    def create_user(
        self,
        nome: str,
        email: str,
        senha: str,
        perfil: str,
        criado_por: int,
    ) -> tuple[bool, str]:
        if perfil not in {"admin", "comum"}:
            return False, "Perfil invalido."
        if len(senha) < 6:
            return False, "Senha deve ter no minimo 6 caracteres."

        senha_hash = generate_password_hash(senha)

        with get_connection(self.database_url) as conn:
            existing = conn.execute(
                "SELECT id FROM usuarios WHERE email = %s", (email,)
            ).fetchone()
            if existing:
                return False, "Email ja cadastrado."

            conn.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo, criado_por)
                VALUES (%s, %s, %s, %s, TRUE, %s)
                """,
                (nome, email, senha_hash, perfil, criado_por),
            )

        return True, "Usuario cadastrado com sucesso."
