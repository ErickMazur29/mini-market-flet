import flet as ft
from database.data import get_connection
from views.home_view import Home

class Historico:
    def __init__(self, page:ft.Page):
        self.page = page

        self.history_list = ft.ListView(
            width=500,
            height=300,
            spacing=5,
        )

        self.product_list = ft.ListView(
            width=400,
            height=250,
            spacing=5,
        )

    def load_history(self):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.window.full_screen = True
        self.page.appbar = ft.AppBar(title=ft.Text("Mini Market", size=25, weight="bold"),)

        self.product_list.controls.clear()

        navigation_tab = ft.Column(
            [
                ft.IconButton(icon = ft.Icons.HOME, on_click= lambda e: Home(self.page).build()),
                ft.IconButton(icon = ft.Icons.HISTORY),
            ]
        )
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT p.nome, p.preco, v.data, v.total FROM itens_venda as iv
            JOIN produtos as p ON iv.id_produto = p.id
            JOIN vendas as v ON iv.id_venda = v.id
            """)
            for p_nome, p_preco, v_data, v_total in cursor.fetchall():

                self.product_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(p_nome, color=ft.Colors.BLACK),
                                ft.Text(f" - ${p_preco}", color=ft.Colors.BLACK)
                            ]
                        ),
                        padding=10,
                        border_radius=8,
                        bgcolor=ft.Colors.BLUE_50,
                    )
                )

                self.history_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"Dia: {v_data} - Total: {v_total}"),
                                self.product_list
                            ]
                        )
                    )
                )

        juntar = ft.Column(
            [
                ft.Text(" HISTÓRICO DE VENDAS ", size=35, weight='bold'),
                ft.Row(
                    controls=[
                        navigation_tab,
                        self.history_list
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20


            )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.add(juntar)
        self.page.update()

