# utils.py
import tkinter as tk
from tkinter import messagebox
import logging

def show_info(msg):
    messagebox.showinfo("Informação", msg)

def show_error(msg):
    messagebox.showerror("Erro", msg)

def confirm(msg):
    return messagebox.askyesno("Confirmação", msg)

def setup_logging():
    logging.basicConfig(filename="app.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
def analisar_pedidos():
    from db import execute
    pedidos = execute("SELECT * FROM pedidos ORDER BY id DESC LIMIT 5", fetchall=True)
    if not pedidos:
        return "Sem pedidos recentes."
    resumo = "\n".join([f"{p['data']}: R$ {p['total']}" for p in pedidos])
    prompt = f"Analise os seguintes pedidos:\n{resumo}\nDiga os produtos mais vendidos e média de valor."
    # Aqui você pode conectar à OpenAI ou Ollama.
    # Por enquanto, retorno simulado:
    return "Insight IA: Ticket médio alto, produtos X e Y mais vendidos."
def analisar_pedidos():
    from db import execute
    pedidos = execute("SELECT * FROM pedidos ORDER BY id DESC LIMIT 5", fetchall=True)
    if not pedidos:
        return "Sem pedidos recentes."
    resumo = "\n".join([f"{p['data']}: R$ {p['total']}" for p in pedidos])
    prompt = f"Analise os seguintes pedidos:\n{resumo}\nDiga os produtos mais vendidos e média de valor."
    # Aqui você pode conectar à OpenAI ou Ollama.
    # Por enquanto, retorno simulado:
    return "Insight IA: Ticket médio alto, produtos X e Y mais vendidos."
