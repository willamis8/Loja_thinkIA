import sqlite3
import logging
from db import get_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_db():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        logging.info("Inicializando banco de dados e criando tabelas...")

        cur.executescript("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unit REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
        """)

        conn.commit()
        logging.info("Tabelas criadas ou já existentes.")

    except Exception as e:
        logging.exception(f"Erro ao inicializar banco de dados: {e}")

    finally:
        if conn:
            conn.close()
