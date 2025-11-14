import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import logging
# CORREÇÃO: Importa a função centralizada
from db import execute


class Relatorios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatórios de Pedidos")
        self.geometry("700x500")

        tk.Label(self, text="Cliente:").pack(anchor="w", padx=10)

        # Conecta ao banco e busca clientes usando a função centralizada
        clientes = execute("SELECT id, nome FROM clientes", fetchall=True)
        self.cliente_map = {c["nome"]: c["id"] for c in clientes if c["nome"] is not None}

        self.cliente_var = tk.StringVar()
        nomes = list(self.cliente_map.keys())
        nomes.insert(0, "Todos os Clientes")  # Opção para buscar todos

        self.cliente_cb = ttk.Combobox(self, textvariable=self.cliente_var, values=nomes, state="readonly")
        self.cliente_cb.set(nomes[0])
        self.cliente_cb.pack(fill="x", padx=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("cliente", "data", "itens", "total"), show="headings")
        for c in self.tree["columns"]:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True, pady=10, padx=10)

        # Botões
        tk.Button(self, text="Filtrar", command=self.filtrar).pack()
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        tk.Button(frame_btns, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Exportar PDF", command=self.exportar_pdf).pack(side="left")

        self.filtrar()  # Carrega dados iniciais

    def filtrar(self):
        nome_cliente = self.cliente_var.get()

        if nome_cliente == "Todos os Clientes":
            cid = None
        else:
            cid = self.cliente_map.get(nome_cliente)

        query = """
                SELECT c.nome, p.data, GROUP_CONCAT(i.produto || ' (' || i.quantidade || ')', '; ') as itens, p.total
                FROM pedidos p
                         JOIN clientes c ON p.cliente_id = c.id
                         LEFT JOIN itens_pedido i ON i.pedido_id = p.id
                WHERE (? IS NULL OR c.id = ?)
                GROUP BY p.id
                ORDER BY p.data DESC \
                """
        # A função execute agora gerencia o tratamento de erros
        rows = execute(query, (cid, cid), fetchall=True)

        self.tree.delete(*self.tree.get_children())
        for r in rows or []:
            cliente, data, itens, total = r["nome"], r["data"], r["itens"], r["total"]
            self.tree.insert("", "end", values=(cliente, data, itens or "", f"R$ {total:.2f}" if total else "R$ 0.00"))

    def exportar_csv(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".csv")
            if not path:
                return
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Cliente", "Data", "Itens", "Total"])
                for i in self.tree.get_children():
                    writer.writerow(self.tree.item(i)["values"])
            messagebox.showinfo("Exportado", f"CSV salvo em {path}")
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Erro", str(e))

    def exportar_pdf(self):
        # Implementação básica de PDF
        try:
            path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if not path:
                return
            c = canvas.Canvas(path, pagesize=A4)
            y = 750
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 780, "Relatório de Pedidos")
            c.setFont("Helvetica", 10)

            headers = ["Cliente", "Data", "Itens", "Total"]
            x_positions = [50, 150, 250, 500]

            # Cabeçalho da tabela no PDF
            for header, x in zip(headers, x_positions):
                c.drawString(x, y, header)
            y -= 15

            # Dados
            for i in self.tree.get_children():
                if y < 50:
                    c.showPage()
                    y = 750
                    c.setFont("Helvetica", 10)

                values = self.tree.item(i)["values"]
                for value, x in zip(values, x_positions):
                    c.drawString(x, y, str(value))
                y -= 15

            c.save()
            messagebox.showinfo("Exportado", f"PDF salvo em {path}")
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Erro", str(e))