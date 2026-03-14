from models.database import get_connection


class ProductModel:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def list_products(self) -> list[dict]:
        with get_connection(self.database_url) as conn:
            rows = conn.execute(
                """
                SELECT id, nome, descricao, preco, quantidade, quantidade_minima,
                       categoria, ativo, data_criacao, data_atualizacao,
                       (quantidade < quantidade_minima) AS baixo_estoque
                FROM produtos
                WHERE ativo = TRUE
                ORDER BY nome
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def get_product(self, product_id: int) -> dict | None:
        with get_connection(self.database_url) as conn:
            row = conn.execute(
                "SELECT * FROM produtos WHERE id = %s AND ativo = TRUE", (product_id,)
            ).fetchone()
        return dict(row) if row else None

    def create_product(self, data: dict, user_id: int) -> tuple[bool, str]:
        valid, message = self._validate_fields(data)
        if not valid:
            return False, message

        with get_connection(self.database_url) as conn:
            existing = conn.execute(
                "SELECT id FROM produtos WHERE nome = %s", (data["nome"],)
            ).fetchone()
            if existing:
                return False, "Ja existe produto com este nome."

            conn.execute(
                """
                INSERT INTO produtos
                (nome, descricao, preco, quantidade, quantidade_minima, categoria, atualizado_por)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["nome"],
                    data.get("descricao", ""),
                    float(data["preco"]),
                    int(data["quantidade"]),
                    int(data["quantidade_minima"]),
                    data.get("categoria", ""),
                    user_id,
                ),
            )
        return True, "Produto cadastrado com sucesso."

    def update_product(self, product_id: int, data: dict, user_id: int) -> tuple[bool, str]:
        valid, message = self._validate_fields(data)
        if not valid:
            return False, message

        with get_connection(self.database_url) as conn:
            existing = conn.execute(
                "SELECT id FROM produtos WHERE nome = %s AND id <> %s",
                (data["nome"], product_id),
            ).fetchone()
            if existing:
                return False, "Ja existe produto com este nome."

            conn.execute(
                """
                UPDATE produtos
                SET nome = %s, descricao = %s, preco = %s, quantidade = %s,
                    quantidade_minima = %s, categoria = %s, data_atualizacao = CURRENT_TIMESTAMP,
                    atualizado_por = %s
                WHERE id = %s AND ativo = TRUE
                """,
                (
                    data["nome"],
                    data.get("descricao", ""),
                    float(data["preco"]),
                    int(data["quantidade"]),
                    int(data["quantidade_minima"]),
                    data.get("categoria", ""),
                    user_id,
                    product_id,
                ),
            )
        return True, "Produto atualizado com sucesso."

    def list_low_stock(self) -> list[dict]:
        with get_connection(self.database_url) as conn:
            rows = conn.execute(
                """
                SELECT id, nome, quantidade, quantidade_minima
                FROM produtos
                WHERE ativo = TRUE AND quantidade < quantidade_minima
                ORDER BY quantidade ASC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _validate_fields(data: dict) -> tuple[bool, str]:
        required_fields = ["nome", "preco", "quantidade", "quantidade_minima"]
        for field in required_fields:
            if not str(data.get(field, "")).strip():
                return False, f"Campo obrigatorio: {field}."

        try:
            preco = float(data["preco"])
            quantidade = int(data["quantidade"])
            quantidade_minima = int(data["quantidade_minima"])
        except ValueError:
            return False, "Preco deve ser numero e quantidades devem ser inteiras."

        if preco <= 0:
            return False, "Preco deve ser maior que zero."
        if quantidade < 0 or quantidade_minima < 0:
            return False, "Quantidades nao podem ser negativas."

        return True, "OK"
