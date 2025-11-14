import tkinter as tk
from tkinter import ttk, messagebox
from db import execute


class Historico(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico de Pedidos - ThinkIA")
        self.geometry("700x450")
        self.resizable(False, False)
        self.configure(bg="#F5F6FA")

        # ====== Estilo ======
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel",
                        font=("Segoe UI", 18, "bold"),
                        background="#F5F6FA")

        style.configure("Search.TEntry",
                        padding=5,
                        font=("Segoe UI", 11))

        style.configure("Treeview",
                        rowheight=28,
                        font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 11, "bold"))

        # ====== Título ======
        title = ttk.Label(self, text="Histórico de Pedidos", style="Title.TLabel")
        title.pack(pady=15)

        # ====== Campo de busca ======
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=20)

        ttk.Label(search_frame, text="Buscar:", font=("Segoe UI", 11)).pack(side="left")

        self.entry_search = ttk.Entry(search_frame, width=30, style="Search.TEntry")
        self.entry_search.pack(side="left", padx=10)
        self.entry_search.bind("<KeyRelease>", self.filtrar)

        # ====== Tabela ======
        self.tree = ttk.Treeview(
            self,
            columns=("id", "cliente", "produto", "valor", "data"),
            show="headings",
            height=12
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("valor", text="Valor (R$)")
        self.tree.heading("data", text="Data")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cliente", width=150)
        self.tree.column("produto", width=150)
        self.tree.column("valor", width=100, anchor="center")
        self.tree.column("data", width=110, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.carregar_dados()

    # ====== Carrega todos os pedidos ======
    def carregar_dados(self):
        self.tree.delete(*self.tree.get_children())

        try:
            rows = execute("SELECT id, cliente, produto, valor, data FROM pedidos", fetchall=True)

            if rows:
                for r in rows:
                    self.tree.insert("", tk.END, values=(r["id"], r["cliente"], r["produto"], r["valor"], r["data"]))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar o banco:\n{e}")

    # ====== Filtro de busca ======
    def filtrar(self, event=None):
        termo = self.entry_search.get().strip()

        self.tree.delete(*self.tree.get_children())

        try:
            rows = execute("""
                SELECT id, cliente, produto, valor, data 
                FROM pedidos 
                WHERE cliente LIKE ? OR produto LIKE ?
            """, (f"%{termo}%", f"%{termo}%"), fetchall=True)

            if rows:
                for r in rows:
                    self.tree.insert("", tk.END, values=(r["id"], r["cliente"], r["produto"], r["valor"], r["data"]))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar o banco:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    Historico(root)
    root.mainloop()
