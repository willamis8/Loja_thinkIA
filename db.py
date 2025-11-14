import sqlite3
import logging
from typing import Optional, List, Any, Tuple

# Configuração do log (garante que o log funciona em todos os arquivos)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_NAME = "app.db"

def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão SQLite com row_factory para acesso por nome da coluna."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

def execute(
    query: str,
    params: Tuple[Any, ...] = (),
    fetchone: bool = False,
    fetchall: bool = False,
    commit: bool = False
) -> Optional[List[sqlite3.Row]]:
    """Executa um comando SQL parametrizado com tratamento de erros."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params)

        if commit:
            conn.commit()
            return None

        if fetchone:
            return cur.fetchone()

        if fetchall:
            return cur.fetchall()

        return None

    except sqlite3.Error as e:
        logging.exception(f"Erro SQL: {e} | Query: {query} | Params: {params}")
        return None

    finally:
        if conn:
            conn.close()