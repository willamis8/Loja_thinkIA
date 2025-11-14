import customtkinter as ctk
from tkinter import messagebox
from db import execute


class ClientesView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Clientes")
        self.geometry("650x450")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")

        # FRAME PRINCIPAL
        main = ctk.CTkFrame(self, corner_radius=15)
        main.pack(expand=True, fill="both", padx=20, pady=20)

        title = ctk.CTkLabel(main, text="Gerenciamento de Clientes", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        # -------- PESQUISA --------
        search_frame = ctk.CTkFrame(main)
        search_frame.pack(fill="x", pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Pesquisar cliente...")
        self.search_entry.pack(side="left", padx=10, fill="x", expand=True)

        btn_pesq = ctk.CTkButton(search_frame, text="Pesquisar", width=100, command=self.pesquisar)
        btn_pesq.pack(side="right", padx=10)

        # -------- LISTAGEM --------
        self.listbox = ctk.CTkTextbox(main, width=580, height=250, corner_radius=10)
        self.listbox.pack(pady=10)

        # -------- CAMPOS --------
        form_frame = ctk.CTkFrame(main)
        form_frame.pack(pady=10)

        self.nome = ctk.CTkEntry(form_frame, placeholder_text="Nome", width=180)
        self.nome.grid(row=0, column=0, padx=10)

        self.email = ctk.CTkEntry(form_frame, placeholder_text="Email", width=180)
        self.email.grid(row=0, column=1, padx=10)

        self.telefone = ctk.CTkEntry(form_frame, placeholder_text="Telefone", width=180)
        self.telefone.grid(row=0, column=2, padx=10)

        # -------- BOTÕES --------
        btns = ctk.CTkFrame(main)
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="Cadastrar", width=150, command=self.cadastrar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns, text="Editar", width=150, command=self.editar).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns, text="Excluir", width=150, command=self.excluir).grid(row=0, column=2, padx=5)

        # Carregar lista ao abrir
        self.load_clientes()

    # ========= FUNÇÕES BANCO =========

    def load_clientes(self):
        self.listbox.delete("1.0", "end")
        data = execute("SELECT * FROM clientes ORDER BY id DESC", fetchall=True)

        if not data:
            self.listbox.insert("end", "Nenhum cliente cadastrado.")
            return

        for c in data:
            self.listbox.insert(
                "end",
                f"ID: {c['id']} | Nome: {c['nome']} | Email: {c['email']} | Telefone: {c['telefone']}\n"
            )

    def pesquisar(self):
        termo = self.search_entry.get().strip()

        if not termo:
            self.load_clientes()
            return

        data = execute(
            "SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ?",
            (f"%{termo}%", f"%{termo}%"),
            fetchall=True
        )

        self.listbox.delete("1.0", "end")

        if not data:
            self.listbox.insert("end", "Nenhum cliente encontrado.")
            return

        for c in data:
            self.listbox.insert(
                "end",
                f"ID: {c['id']} | Nome: {c['nome']} | Email: {c['email']} | Tel: {c['telefone']}\n"
            )

    def cadastrar(self):
        nome = self.nome.get().strip()
        email = self.email.get().strip()
        telefone = self.telefone.get().strip()

        if not nome:
            messagebox.showwarning("Erro", "O nome é obrigatório.")
            return

        execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone),
            commit=True
        )

        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        self.clear_fields()
        self.load_clientes()

    def editar(self):
        try:
            linha = self.listbox.get("insert linestart", "insert lineend")
            cid = linha.split("|")[0].replace("ID:", "").strip()
        except:
            messagebox.showwarning("Erro", "Selecione um cliente clicando na linha.")
            return

        nome = self.nome.get().strip()
        email = self.email.get().strip()
        telefone = self.telefone.get().strip()

        if not nome:
            messagebox.showwarning("Erro", "O nome é obrigatório.")
            return

        execute(
            "UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?",
            (nome, email, telefone, cid),
            commit=True
        )

        messagebox.showinfo("Sucesso", "Cliente atualizado!")
        self.clear_fields()
        self.load_clientes()

    def excluir(self):
        try:
            linha = self.listbox.get("insert linestart", "insert lineend")
            cid = linha.split("|")[0].replace("ID:", "").strip()
        except:
            messagebox.showwarning("Erro", "Selecione um cliente clicando na linha.")
            return

        execute("DELETE FROM clientes WHERE id=?", (cid,), commit=True)

        messagebox.showinfo("Sucesso", "Cliente excluído!")
        self.load_clientes()

    def clear_fields(self):
        self.nome.delete(0, "end")
        self.email.delete(0, "end")
        self.telefone.delete(0, "end")
