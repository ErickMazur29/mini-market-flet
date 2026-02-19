import flet as ft
from services.history_service import pegar_historico
from services.sale_service import existe_historico_vendas
from components.navbar import _navigation_home #navegação para home
from components.navbar import _appbar #appbar

class Historico:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.history_list = ft.ListView(
            width=1000,
            height=700,
            spacing=5,
        )

    def load_history(self):
        self.history_list.controls.clear()

        vendas = pegar_historico()


        for venda in vendas:

            product_list = ft.ListView(
                width=600,
                height=300,
                spacing=5,
            )

            
            for nome, preco in venda["produtos"]:
                product_list.controls.append(
                    ft.Text(f"{nome} - RS {preco: .2f}", color=ft.Colors.BLACK)
                )

            self.history_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Data: {venda["data"]}", weight="bold"),
                            ft.Text(f"Total: R${venda["total"]}", weight="bold"),
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
        
        self.page.appbar = _appbar("Mini Market Flet")

        

        navigation_tab = _navigation_home(lambda e: self.router.go("home", Home))
        

        juntar = ft.Column(
            [
                ft.Text(" HISTÓRICO DE VENDAS ", size=35, weight='bold'),
                ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
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

