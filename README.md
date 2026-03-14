# Criando uma aplicacao de controle de estoque

Aplicacao web em Python com Flask para controle de entrada e saida de produtos e materiais.

## Funcionalidades principais

- Login e senha com sessao de usuario
- Perfis: `admin` e `comum`
- Somente admin pode cadastrar novos usuarios
- Cadastro e edicao de produtos
- Movimentacao de estoque (entrada e saida)
- Alertas visuais para produtos abaixo da quantidade minima
- Persistencia em banco PostgreSQL
- Senhas salvas com hash (`werkzeug.security`)

## Estrutura

```text
.
├── app.py
├── config.py
├── docker-compose.yml
├── requirements.txt
├── models/
├── routes/
├── templates/
├── static/
├── database/
│   └── schema.sql
└── docs/
```

## Como executar

1. Configure variaveis de ambiente:

```bash
cp .env.example .env
```

2. Suba o banco PostgreSQL via Docker Compose:

```bash
docker compose up -d db
```

3. Criar ambiente virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Instalar dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Iniciar aplicacao:

```bash
python app.py
```

6. Abrir no navegador:

```text
http://127.0.0.1:5000
```

## Usuario inicial

- Email: `admin@estoque.local`
- Senha: `admin123`

## Requisitos do desafio cobertos

- Modelagem de dados: `database/schema.sql` e `docs/modelo_dados.md`
- Fluxograma: `docs/fluxograma.md`
- Interface para navegacao: templates Flask
- Validacoes de campos: front-end (`static/js/validations.js`) e back-end (models)
- Sessao, login/senha e perfis
- Conexao com banco de dados PostgreSQL
- Alerta de baixo estoque na listagem e dashboard

## Empacotamento para entrega

Gerar um ZIP contendo todo o projeto (exceto venv e cache).

## Banco de dados

- O schema esta em `database/schema.sql`.
- Na primeira inicializacao, o sistema aplica o schema e cria o usuario admin padrao.
- Conexao configurada por `DATABASE_URL` (arquivo `.env`).
- Porta padrao do PostgreSQL no compose: `5433` (para evitar conflito com instalacoes locais em `5432`).

## Observacao (PEP 668)

Se aparecer `externally-managed-environment`, voce esta usando o `pip` do sistema.
Use sempre o ambiente virtual do projeto:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```
