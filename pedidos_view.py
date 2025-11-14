import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
# CORREÇÃO: Importação absoluta para o db.py na raiz
from db import execute


# from views.dashboard_view import Dashboard # Não é necessário aqui, foi removido

class PedidoForm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Novo Pedido")
        self.geometry("600x400")

        # Busca clientes e mapeia para fácil acesso
        self.clientes = execute("SELECT id, nome FROM clientes ORDER BY nome", fetchall=True)

        tk.Label(self, text="Cliente:").pack(anchor="w", padx=10, pady=(10, 0))
        self.cliente_var = tk.StringVar()
        nomes = [c["nome"] for c in self.clientes]
        self.cliente_cb = ttk.Combobox(self, values=nomes, textvariable=self.cliente_var, state="readonly")
        self.cliente_cb.pack(fill="x", padx=10)

        tk.Label(self, text="Data:").pack(anchor="w", padx=10, pady=(10, 0))
        self.data_var = tk.StringVar(value=str(date.today()))
        tk.Entry(self, textvariable=self.data_var).pack(fill="x", padx=10)

        # tabela de itens
        cols = ("produto", "quantidade", "preco_unit")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=5)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack()
        tk.Button(btns, text="Adicionar Item", command=self.add_item).pack(side="left", padx=5)
        tk.Button(btns, text="Remover Item", command=self.del_item).pack(side="left", padx=5)

        self.total_var = tk.StringVar(value="0.00")
        tk.Label(self, text="Total:").pack(anchor="e", padx=10)
        tk.Label(self, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(anchor="e", padx=10)

        tk.Button(self, text="Salvar Pedido", command=self.salvar).pack(pady=10)

    def add_item(self):
        item_win = tk.Toplevel(self)
        item_win.title("Adicionar Item")
        item_win.transient(self)  # Mantém no topo
        item_win.grab_set()  # Bloqueia a janela principal

        tk.Label(item_win, text="Produto:").pack()
        produto = tk.Entry(item_win)
        produto.pack()
        tk.Label(item_win, text="Quantidade:").pack()
        qtd = tk.Entry(item_win)
        qtd.pack()
        tk.Label(item_win, text="Preço unitário:").pack()
        preco = tk.Entry(item_win)
        preco.pack()

        def confirmar():
            try:
                q = int(qtd.get())
                p = float(preco.get())

                if q <= 0 or p <= 0:
                    raise ValueError("Quantidade e preço devem ser positivos.")

                # Atualiza total
                current_total = float(self.total_var.get())
                new_total = current_total + (q * p)
                self.total_var.set(f"{new_total:.2f}")

                # Insere na tabela (Treeview)
                self.tree.insert("", "end", values=(produto.get(), q, p))
                item_win.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos para Quantidade/Preço.")

        tk.Button(item_win, text="OK", command=confirmar).pack(pady=10)

    def del_item(self):
        sel = self.tree.selection()
        if not sel:
            return

        current_total = float(self.total_var.get())

        for s in sel:
            vals = self.tree.item(s)["values"]
            qtd = vals[1]
            preco = vals[2]
            current_total -= (qtd * preco)
            self.tree.delete(s)

        self.total_var.set(f"{current_total:.2f}")

    def salvar(self):
        nome = self.cliente_var.get()
        # Encontra o ID do cliente selecionado
        cliente = next((c for c in self.clientes if c["nome"] == nome), None)

        if not cliente:
            messagebox.showwarning("Validação", "Selecione um cliente.")
            return

        if not self.tree.get_children():
            messagebox.showwarning("Validação", "Adicione pelo menos um item ao pedido.")
            return

        data = self.data_var.get()
        total = float(self.total_var.get())

        # O execute já gerencia a conexão, vamos fazer as operações sequencialmente.
        # Poderíamos usar transações explícitas, mas o commit=True em cada execute funciona
        # para operações simples. Para um cenário mais robusto, um método de transação seria melhor.
        try:
            # 1. Salva o pedido
            execute("INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
                    (cliente["id"], data, total), commit=True)

            # 2. Pega o ID do pedido recém-criado
            pedido = execute("SELECT last_insert_rowid() as id", fetchone=True)
            pedido_id = pedido["id"]

            # 3. Salva os itens do pedido
            for i in self.tree.get_children():
                prod, qtd, preco = self.tree.item(i)["values"]
                execute("""INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit)
                           VALUES (?, ?, ?, ?)""",
                        (pedido_id, prod, qtd, preco), commit=True)

            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            self.destroy()
        except Exception as e:
            # Em caso de falha, o log registra o erro e o usuário é notificado.
            messagebox.showerror("Erro", f"Falha ao salvar pedido: {e}")