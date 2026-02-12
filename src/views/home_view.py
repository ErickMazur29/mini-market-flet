import flet as ft
from services.cart_service import calculate_total
from services.sale_service import finalize_sale
from services.product_service import get_all_products
from components.navbar import _navigation
from components.navbar import _appbar
from components.card import card_padrao_home
from components.card import style_cart_list
from components.card import style_product_list


class Home:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.products_loaded = False
        self.selected_product = None #clicar na lista de produtos
        self.selected_product_control = None #controlador para ver se esta clicado ou nao
        self.selected_card_product = None #clicar na lista de compras
        self.selected_cart_control = None #controlador para ver se esta clicado ou nao

        self.total_text = ft.Text("Total: $0.00", size=18, weight="bold", color=ft.Colors.BLACK_26)

        self.product_list = ft.ListView(
            width=400,
            height=250,
            spacing=5,
        )

        self.cart_list = ft.ListView(
            width=400,
            height=200,
            spacing=5,
            
            
        )


    def load_products(self):
        self.product_list.controls.clear()

        for product_id, name, price in get_all_products():
            self.product_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(name, color=ft.Colors.BLACK),
                            ft.Text(f" - ${price}", color=ft.Colors.BLACK)
                        ]
                    ),
                    padding=10,
                    border_radius=8,
                    bgcolor=ft.Colors.BLUE_50,
                    data={"id": product_id, "name": name, "price": price},
                    on_click=self.select_product
                )
            )

    def select_product(self, e):
        if self.selected_product_control == e.control:
            e.control.bgcolor = ft.Colors.BLUE_50
            self.selected_product_control = None
            self.selected_product = None
            self.page.update()
            return

        for item in self.product_list.controls:
            item.bgcolor = ft.Colors.BLUE_50

        e.control.bgcolor = ft.Colors.BLUE_200
        self.selected_product_control = e.control
        self.selected_product = e.control.data
        self.page.update()



    # ================= CARRINHO =================

    def add_to_cart(self, e):
        if not self.selected_product:
            self.show_snack("Selecione um produto!")
            return

        item_text = f"{self.selected_product['name']} - ${self.selected_product['price']}"

        self.cart_list.controls.append(
            ft.Container(
                content=ft.Text(item_text, color=ft.Colors.BLACK),
                padding=8,
                border_radius=6,
                bgcolor=ft.Colors.GREEN_50,
                data=self.selected_product,
                on_click=self.select_card_item
            )
        )
        self.sum_cart_list()
        self.page.update()


    def select_card_item(self, e):
        if self.selected_cart_control == e.control:
            e.control.bgcolor = ft.Colors.GREEN_50
            self.selected_cart_control = None
            self.selected_card_product = None
            self.page.update()


            return

        for item in self.cart_list.controls:
            item.bgcolor = ft.Colors.GREEN_50

        e.control.bgcolor = ft.Colors.GREEN_200
        self.selected_cart_control = e.control
        self.selected_card_product = e.control.data
        self.page.update()



    def remove_from_cart(self, e):
        if not self.selected_cart_control:
            self.show_snack("Selecione um item do carrinho!")
            return

        self.cart_list.controls.remove(self.selected_cart_control)
        self.selected_cart_control = None
        self.selected_card_product = None
        self.sum_cart_list()
        self.page.update()

    # ================= SOMA TOTAL =================

    def sum_cart_list(self):
        total = calculate_total(item.data for item in self.cart_list.controls)
        self.total_text.value = f"Total: {total:.2f}"

    # =============== NOTIFICAÇÃO ================

    def show_snack(self, msg):
        snack = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def show_snack_final(self, msg):
        snack = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    # ============FINALIZAR COMPRA ===============

    def finalizar_compra(self, e):
        if len(self.cart_list.controls) == 0:
            self.show_snack("O carrinho esta vazio!")
            return
        
        cart_items = [item.data for item in self.cart_list.controls]
        finalize_sale(cart_items)

        #limpa carrinho
        self.cart_list.controls.clear() 
        self.total_text.value = "Total: 0.00 "
        self.select_cart_control = None
        self.selected_card_product = None

        self.show_snack_final("Venda finalizada com sucesso!")
        self.page.update()

    # ================= BUILD ====================

    def build(self):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.window.full_screen = True
        from views.history_view import Historico

        if not self.products_loaded:
            self.load_products()
            self.products_loaded = True

        appbar = _appbar("Mini Market Flet")
        navegacao = _navigation(lambda e: self.router.go("history", Historico))

        # ================= CARD PRODUTOS =================

        home_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Faça o pedido do cliente!",
                        size=24,
                        weight="bold",
                        color=ft.Colors.BLACK_87
                    ),

                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),

                    ft.Container(
                        content=self.product_list,
                        width=400,
                        height=300,
                        padding=10,
                        margin=ft.Margin.only(top=10, bottom=10),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=12,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                    ),

                    ft.Button(
                        "ADICIONAR PRODUTO",
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=self.add_to_cart
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12
            ),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            width=350,
            height=600,
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        )

        # ================= CARD CARRINHO =================

        cart_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Carrinho",
                        size=24,
                        weight="bold",
                        color=ft.Colors.BLACK_87
                    ),

                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),

                    ft.Container(
                        content=self.cart_list,
                        width=400,
                        height=300,
                        padding=10,
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=12,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                    ),

                    ft.Divider(height=15, color=ft.Colors.BLACK),

                    ft.Button(
                        "REMOVER PRODUTO",
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=self.remove_from_cart
                    ),

                    ft.Button(
                        "FINALIZAR COMPRA",
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=self.finalizar_compra
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12
            ),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            width=350,
            height=600,
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        )

        # ================= LAYOUT =================

        layout = ft.Column(
            [
                ft.Text(" MERCADINHO FLET ", size=35, weight='bold'),
                ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        navegacao,
                        home_card,
                        cart_card
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.add(layout)
        self.page.update()

