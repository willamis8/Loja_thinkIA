import tkinter as tk
from tkinter import Frame, Label, Button, messagebox
from db import execute


class Dashboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Dashboard")
        self.geometry("650x400")
        self.resizable(False, False)

        # ---------------- ESTILO ----------------
        self.bg_main = "#1e1e1e"       # fundo principal
        self.bg_card = "#2b2b2b"       # fundo dos cards
        self.fg_text = "#ffffff"       # texto branco
        self.btn_color = "#3a7ff6"     # azul moderno

        self.configure(bg=self.bg_main)

        # ---------------- TÍTULO ----------------
        title = Label(
            self,
            text="Dashboard",
            font=("Arial", 26, "bold"),
            bg=self.bg_main,
            fg=self.fg_text
        )
        title.pack(pady=20)

        # ---------------- CARDS ----------------
        cards_frame = Frame(self, bg=self.bg_main)
        cards_frame.pack(pady=10)

        self.card_clientes = self.create_card(
            cards_frame, "Clientes", self.count_clientes()
        )
        self.card_clientes.grid(row=0, column=0, padx=20)

        self.card_pedidos = self.create_card(
            cards_frame, "Pedidos", self.count_pedidos()
        )
        self.card_pedidos.grid(row=0, column=1, padx=20)

        self.card_vendas = self.create_card(
            cards_frame, "Total Vendido (R$)", self.sum_total_vendido()
        )
        self.card_vendas.grid(row=0, column=2, padx=20)

        # ---------------- BOTÕES ----------------
        btn_frame = Frame(self, bg=self.bg_main)
        btn_frame.pack(pady=25)

        Button(
            btn_frame,
            text="Gerenciar Clientes",
            width=20,
            bg=self.btn_color,
            fg="white",
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=0, padx=12)

        Button(
            btn_frame,
            text="Gerenciar Pedidos",
            width=20,
            bg=self.btn_color,
            fg="white",
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=1, padx=12)

        Button(
            self,
            text="Atualizar Dashboard",
            width=30,
            bg=self.btn_color,
            fg="white",
            relief="flat",
            command=self.update_dashboard,
            cursor="hand2"
        ).pack(pady=10)

    # ---------------- BANCO DE DADOS ----------------

    def count_clientes(self):
        r = execute("SELECT COUNT(*) AS total FROM clientes", fetchone=True)
        return r["total"] if r else 0

    def count_pedidos(self):
        r = execute("SELECT COUNT(*) AS total FROM pedidos", fetchone=True)
        return r["total"] if r else 0

    def sum_total_vendido(self):
        r = execute("SELECT SUM(total) AS soma FROM pedidos", fetchone=True)
        return f"{r['soma']:.2f}" if r and r["soma"] else "0.00"

    # ---------------- UI HELPERS ----------------

    def create_card(self, parent, title, value):
        frame = Frame(parent, bg=self.bg_card, width=170, height=120)
        frame.grid_propagate(False)
        frame.configure(highlightbackground="#444", highlightthickness=1)

        Label(
            frame,
            text=title,
            font=("Arial", 14),
            bg=self.bg_card,
            fg=self.fg_text
        ).pack(pady=5)

        Label(
            frame,
            text=str(value),
            font=("Arial", 22, "bold"),
            bg=self.bg_card,
            fg=self.fg_text
        ).pack()

        return frame

    # ---------------- ATUALIZAR UI ----------------

    def update_dashboard(self):

        self.card_clientes.destroy()
        self.card_pedidos.destroy()
        self.card_vendas.destroy()

        cards_frame = self.winfo_children()[1]  # segundo frame

        self.card_clientes = self.create_card(
            cards_frame, "Clientes", self.count_clientes()
        )
        self.card_clientes.grid(row=0, column=0, padx=20)

        self.card_pedidos = self.create_card(
            cards_frame, "Pedidos", self.count_pedidos()
        )
        self.card_pedidos.grid(row=0, column=1, padx=20)

        self.card_vendas = self.create_card(
            cards_frame, "Total Vendido (R$)", self.sum_total_vendido()
        )
        self.card_vendas.grid(row=0, column=2, padx=20)

        messagebox.showinfo("Atualizado", "Dashboard atualizado com sucesso!")
