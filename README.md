# FirebirdAPI

FirebirdAPI é uma API REST construída com Python e FastAPI para consultas de leitura (somente `SELECT`) em um banco de dados Firebird. A API aplica paginação obrigatória em todas as consultas, permitindo acesso seguro e eficiente aos dados sem necessidade de modificar diretamente o banco.

## Pré-requisitos

- **Python 3.8+**
- **Firebird** (Banco de dados)
- **Dependências do Python**:
  - FastAPI
  - Firebird-driver
  - Python-dotenv
  - Uvicorn (para executar a API)

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu_usuario/FirebirdAPI.git
   cd FirebirdAPI
   ```

2. Instale as dependências:
   ```bash
   pip install fastapi uvicorn firebird-driver python-dotenv
   ```

3. Crie um arquivo `.env` para configurar as credenciais de conexão com o banco de dados Firebird. No diretório principal do projeto, crie o arquivo `.env` com o seguinte conteúdo:

   ```plaintext
   DB_DSN=localhost:/caminho/para/seu/banco.fdb
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

   - **DB_DSN**: DSN do banco de dados Firebird (por exemplo, `localhost:/path/to/your/database.fdb`).
   - **DB_USER**: Usuário do banco de dados.
   - **DB_PASSWORD**: Senha do banco de dados.

## Execução

Para iniciar o servidor, execute:

```bash
uvicorn app:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

## Uso

A API possui um endpoint principal para consultas SQL de leitura com paginação.

### Endpoint `/execute`

**POST** `/execute`

- **Descrição**: Executa uma consulta `SELECT` no banco de dados Firebird, retornando os dados paginados.
- **Parâmetros de Query**:
  - `limit` (int, opcional, padrão: 10): Limita o número de registros retornados. Mínimo: 1, Máximo: 100.
  - `offset` (int, opcional, padrão: 0): Define o ponto inicial para os registros.
- **Corpo da Requisição** (JSON):
  - `query` (string): Consulta SQL `SELECT` a ser executada. **Somente consultas `SELECT` são permitidas.**

**Exemplo de Requisição**:

```http
POST http://127.0.0.1:8000/execute?limit=10&offset=20
Content-Type: application/json

{
    "query": "SELECT * FROM sua_tabela"
}
```

**Exemplo de Resposta**:

```json
{
    "resultados": [
        {"coluna1": "valor1", "coluna2": "valor2"},
        {"coluna1": "valor3", "coluna2": "valor4"}
    ],
    "limit": 10,
    "offset": 20
}
```

### Regras de Segurança

1. **Somente Consultas `SELECT`**: A API permite apenas comandos `SELECT`. Consultas contendo `INSERT`, `DELETE`, `UPDATE`, `CREATE`, `DROP`, entre outras, serão rejeitadas com um erro de autorização.
2. **Paginação Obrigatória**: Todas as consultas devem incluir `limit` e `offset`, controlando o número de registros retornados e o ponto de início dos dados.

### Logging

- A API registra todas as requisições em um arquivo `app.log`, mantendo apenas as últimas 1000 linhas.
- Tentativas de consultas não permitidas e erros são registrados com o nível `WARNING` ou `ERROR`.

## Estrutura do Código

```plaintext
.
├── .env                # Configurações de conexão com o banco
├── app.py              # Código principal da API
├── app.log             # Arquivo de logs (criado automaticamente)
└── README.md           # Documentação do projeto
```

## Executando Testes

Para testar a API, você pode usar ferramentas como **Postman** ou **curl**. Abaixo está um exemplo com `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/execute?limit=10&offset=0" \
-H "Content-Type: application/json" \
-d "{\"query\": \"SELECT * FROM sua_tabela\"}"
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou _pull request_ com melhorias, correções de bugs, ou novas funcionalidades.

---

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

--- 

### Observações

Esse projeto serve como uma camada de API somente leitura para bancos Firebird e deve ser utilizado em ambientes controlados. Certifique-se de revisar os logs e monitorar o uso para garantir a segurança e o desempenho.