import flet as ft
from database.data import get_connection
from services.vendas_service import existe_historico_vendas

class Historico:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.history_list = ft.ListView(
            width=1500,
            height=700,
            spacing=5,
        )

    def load_history(self):
        self.history_list.controls.clear()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, data, total FROM vendas ORDER BY id DESC")
            vendas = cursor.fetchall()
            for venda_id, venda_data, venda_total in vendas:

                product_list = ft.ListView(
                    width=600,
                    height=300,
                    spacing=5,
                )

                cursor.execute("""
                    SELECT p.nome, iv.preco FROM itens_venda as iv
                    JOIN produtos p ON p.id = iv.id_produto
                    WHERE iv.id_venda = ? 
                    """, (venda_id,))
                
                for nome, preco in cursor.fetchall():
                    product_list.controls.append(
                        ft.Text(f"{nome} - RS {preco: .2f}", color=ft.Colors.BLACK)
                    )

                self.history_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"Data: {venda_data}", weight="bold"),
                                ft.Text(f"Total: R${venda_total}", weight="bold"),
                                product_list
                            ]
                        ),
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_100,
                    border=ft.Border.all(1, ft.Colors.GREY_300)
                    )
                )


        

    def build(self):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.window.full_screen = True
        self.page.appbar = ft.AppBar(title=ft.Text("Mini Market", size=25, weight="bold"),)

        self.load_history()
        
        from views.home_view import Home

        if not existe_historico_vendas():
            self.page.add(
                ft.Text(
                    "Não há histórico ainda.",
                    size=30,
                    weight="bold",
                ),
                ft.Button(
                    "Voltar",
                    on_click=lambda e: self.router.go("home", Home)
                )
            )
            self.page.update()
            return

        

        navigation_tab = ft.Column(
            [
                ft.IconButton(icon = ft.Icons.HOME, on_click=lambda e: self.router.go("home", Home)),
                ft.IconButton(icon = ft.Icons.HISTORY),
            ]
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

