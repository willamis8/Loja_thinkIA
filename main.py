# ...existing code...
import customtkinter as ctk
from init_db import init_db
from dashboard_view import Dashboard
from clientes_view import ClientesView


def main():
    init_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("ThinkIA - Sistema")
    root.geometry("400x300")
    root.resizable(False, False)

    title = ctk.CTkLabel(root, text="ThinkIA - Sistema", font=("Arial", 26, "bold"))
    title.pack(pady=20)

    btn_dashboard = ctk.CTkButton(
        root,
        text="Abrir Dashboard",
        width=220,
        command=lambda: Dashboard(root)
    )
    btn_dashboard.pack(pady=10)

    btn_clientes = ctk.CTkButton(
        root,
        text="Gerenciar Clientes",
        width=220,
        command=lambda: ClientesView(root)
    )
    btn_clientes.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
# ...existing code...