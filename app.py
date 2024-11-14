import os
import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import firebird.driver as fdb
import re

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logger para manter as últimas 1000 linhas de log
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
log_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=1024*1000, backupCount=1)
logging.getLogger().addHandler(log_handler)

# Configurações de conexão com o banco de dados Firebird
DATABASE_CONFIG = {
    "dsn": os.getenv("DB_DSN"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

# Lista de palavras-chave proibidas para consultas de leitura
PROHIBITED_KEYWORDS = [
    r"\bINSERT\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bCREATE\b", r"\bDROP\b",
    r"\bALTER\b", r"\bEXECUTE\b", r"\bMERGE\b", r"\bREPLACE\b", r"\bTRUNCATE\b"
]

def is_query_safe(query: str) -> bool:
    """
    Verifica se a consulta contém apenas comandos de leitura (SELECT).
    Retorna False se palavras-chave proibidas forem encontradas.
    """
    query_upper = query.upper()
    for keyword in PROHIBITED_KEYWORDS:
        if re.search(keyword, query_upper):
            return False
    return True

def execute_select_query(query: str, limit: int, offset: int):
    """
    Executa uma consulta SELECT no banco de dados Firebird com paginação.
    Adiciona LIMIT e OFFSET na consulta para garantir paginação.
    """
    if not query.strip().lower().startswith("select") or not is_query_safe(query):
        logging.warning("Tentativa de execução de uma consulta não autorizada: %s", query)
        raise ValueError("Apenas consultas SELECT são permitidas.")

    # Adiciona LIMIT e OFFSET à consulta
    paginated_query = f"{query.strip()} LIMIT {limit} OFFSET {offset}"

    try:
        with fdb.connect(**DATABASE_CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute(paginated_query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Nomes das colunas
            logging.info("Consulta executada com sucesso: %s", paginated_query)
            return [dict(zip(columns, row)) for row in results]  # Retorna como lista de dicionários
    except Exception as e:
        logging.error("Erro ao executar consulta: %s - Erro: %s", paginated_query, str(e))
        raise

@app.post("/execute")
async def execute(
    request: QueryRequest,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Endpoint para consultas com paginação.
    - limit: Limita o número de registros retornados (padrão: 10, máximo: 100).
    - offset: Define o ponto inicial para os registros (padrão: 0).
    """
    try:
        resultados = execute_select_query(request.query, limit, offset)
        return {"resultados": resultados, "limit": limit, "offset": offset}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados.")
