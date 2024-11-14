# FirebirdAPI

FirebirdAPI é uma API em Python criada com FastAPI que fornece uma camada de acesso de leitura ao banco de dados Firebird. Esta API permite a execução de consultas `SELECT` de forma segura, rejeitando comandos que possam modificar o banco de dados.

## Requisitos

- Python 3.7 ou superior
- Banco de dados Firebird
- Dependências do projeto listadas em `requirements.txt`

## Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/lippelima5/firebirdapi.git
   cd firebirdapi
   ```

2. **Instale as dependências**

   No diretório do projeto, execute:

   ```bash
   pip install -r requirements.txt
   ```

   O arquivo `requirements.txt` contém as bibliotecas necessárias:

   ```
   fastapi
   uvicorn
   python-dotenv
   firebird-driver
   ```

## Configuração do Banco de Dados

Crie um arquivo `.env` na raiz do projeto para armazenar as credenciais do banco de dados Firebird. Esse arquivo deve conter as seguintes variáveis:

```plaintext
DB_DSN=localhost:/caminho/para/seu/banco.fdb
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

- **DB_DSN**: String de conexão com o banco de dados (ex: `localhost:/path/to/your/database.fdb`).
- **DB_USER**: Nome de usuário para acessar o banco de dados.
- **DB_PASSWORD**: Senha do usuário do banco de dados.

> **Nota:** Certifique-se de manter o arquivo `.env` seguro, pois ele contém informações sensíveis.

## Executando o Servidor

Após configurar o arquivo `.env`, você pode iniciar o servidor com o comando:

```bash
uvicorn app:app --reload
```

O servidor estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Utilização

### Endpoint `/execute`

O endpoint principal `/execute` permite executar consultas `SELECT` no banco de dados Firebird.

- **Método**: POST
- **Parâmetros**: JSON no formato `{"query": "SELECT * FROM sua_tabela"}`

#### Exemplo de Solicitação

Faça uma requisição POST ao endpoint com uma consulta:

```http
POST http://127.0.0.1:8000/execute
Content-Type: application/json

{
    "query": "SELECT * FROM sua_tabela"
}
```

#### Exemplo de Resposta

```json
{
    "result": [
        {
            "coluna1": "valor1",
            "coluna2": "valor2"
        },
        ...
    ]
}
```

### Observação de Segurança

- Somente consultas `SELECT` são permitidas.
- Comandos de modificação de dados, como `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, etc., são bloqueados e resultam em erro.

### Logs

A API mantém um arquivo de log (`app.log`) com os registros das consultas executadas e tentativas não autorizadas. Os logs são limitados às últimas 1000 linhas para evitar o crescimento excessivo do arquivo.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou _pull request_ com melhorias, correções de bugs, ou novas funcionalidades.
