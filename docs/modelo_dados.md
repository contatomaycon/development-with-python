# Modelagem de dados

## Entidades

### usuarios
- `id` (PK)
- `nome` (obrigatorio)
- `email` (obrigatorio, unico)
- `senha_hash` (obrigatorio)
- `perfil` (`admin` ou `comum`)
- `ativo`
- `data_criacao`
- `criado_por` (FK para `usuarios.id`)

### produtos
- `id` (PK)
- `nome` (obrigatorio, unico)
- `descricao`
- `preco` (> 0)
- `quantidade` (>= 0)
- `quantidade_minima` (>= 0)
- `categoria`
- `ativo`
- `data_criacao`
- `data_atualizacao`
- `atualizado_por` (FK para `usuarios.id`)

### movimentacoes
- `id` (PK)
- `produto_id` (FK para `produtos.id`)
- `tipo` (`entrada` ou `saida`)
- `quantidade` (> 0)
- `usuario_id` (FK para `usuarios.id`)
- `motivo`
- `data_movimentacao`

## Relacionamentos

- Um usuario pode criar varios usuarios (`usuarios.criado_por`).
- Um usuario pode atualizar varios produtos (`produtos.atualizado_por`).
- Um produto pode ter varias movimentacoes.
- Um usuario pode registrar varias movimentacoes.

## Regras de integridade

- Nao aceita preco <= 0.
- Nao aceita quantidades negativas.
- Nao permite duplicidade de email em usuarios.
- Nao permite duplicidade de nome de produto.
- Nao permite saldo de produto negativo na saida.
