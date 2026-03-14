from models.database import get_connection


class MovementModel:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def register_movement(
        self,
        product_id: int,
        tipo: str,
        quantidade: int,
        usuario_id: int,
        motivo: str,
    ) -> tuple[bool, str]:
        if tipo not in {"entrada", "saida"}:
            return False, "Tipo de movimentacao invalido."
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."

        with get_connection(self.database_url) as conn:
            product = conn.execute(
                "SELECT id, quantidade FROM produtos WHERE id = %s AND ativo = TRUE",
                (product_id,),
            ).fetchone()
            if not product:
                return False, "Produto nao encontrado."

            saldo_atual = int(product["quantidade"])
            novo_saldo = saldo_atual + quantidade if tipo == "entrada" else saldo_atual - quantidade

            if novo_saldo < 0:
                return False, "Saida maior que saldo disponivel."

            conn.execute(
                "UPDATE produtos SET quantidade = %s, data_atualizacao = CURRENT_TIMESTAMP, atualizado_por = %s WHERE id = %s",
                (novo_saldo, usuario_id, product_id),
            )
            conn.execute(
                """
                INSERT INTO movimentacoes (produto_id, tipo, quantidade, usuario_id, motivo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (product_id, tipo, quantidade, usuario_id, motivo),
            )

        return True, "Movimentacao registrada com sucesso."

    def list_movements(self) -> list[dict]:
        with get_connection(self.database_url) as conn:
            rows = conn.execute(
                """
                SELECT m.id, p.nome AS produto_nome, m.tipo, m.quantidade,
                       u.nome AS usuario_nome, m.motivo, m.data_movimentacao
                FROM movimentacoes m
                JOIN produtos p ON p.id = m.produto_id
                JOIN usuarios u ON u.id = m.usuario_id
                ORDER BY m.data_movimentacao DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]
