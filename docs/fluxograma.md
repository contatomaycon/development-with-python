# Fluxograma da aplicacao

```text
INICIO
  |
  v
[Login]
  |-- credenciais invalidas --> [Mensagem de erro] --> [Login]
  |-- credenciais validas --> [Criar sessao]
                               |
                               v
                         [Dashboard]
                               |
          +--------------------+-------------------+
          |                                        |
          v                                        v
   [Listar produtos]                        [Usuarios] (apenas admin)
          |                                        |
          |                               [Cadastrar usuario]
          |
          +--> [Cadastrar produto] (admin)
          |
          +--> [Editar produto] (admin)
          |
          +--> [Movimentar estoque] (admin)
                 | entrada/saida
                 v
          [Atualiza saldo + grava historico]

[Logout] --> [Encerrar sessao] --> [Login]
```

## Regras de negocio no fluxo

- Usuario comum: visualiza dashboard e estoque.
- Usuario admin: pode cadastrar usuario, cadastrar/editar produto e registrar movimentacao.
- Produtos com quantidade abaixo do minimo sao destacados na interface.
