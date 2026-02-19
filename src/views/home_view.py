import flet as ft
from services.cart_service import calculate_total
from services.sale_service import finalize_sale 
from services.product_service import get_all_products 
from components.navbar import _navigation_history #navegação para historico
from components.navbar import _appbar 
from components.card import card_padrao_home #estilo de card
from components.card import style_cart_list #estilo de list
from components.card import style_product_list #estilo de list
from components.card import list_text #estilo de list text
from utils.notifications import build_snack #notificação
from components.button import botao_padrao_home #estilo dos botões
from utils.constants import ButtonType #cor dos botoes



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

    #carregar os produtos na listview
    def load_products(self):
        self.product_list.controls.clear()

        for product_id, name, price in get_all_products():
            self.product_list.controls.append(
                list_text(
                    ft.Text(f"{name} - ${price}", color=ft.Colors.BLACK),
                    {"id": product_id, "name": name, "price": price},
                    ft.Colors.BLUE_50,
                    self.select_product,
                ),
            )


    #selecionar os produtos da list
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

    #adicionar o carrinho
    def add_to_cart(self, e):
        if not self.selected_product:
            build_snack(self.page,"Selecione um produto!")
            return

        item_text = f"{self.selected_product['name']} - ${self.selected_product['price']}"

        self.cart_list.controls.append(

            list_text(
                    ft.Text(item_text, color=ft.Colors.BLACK),
                    self.selected_product,
                    ft.Colors.GREEN_50,
                    self.select_card_item,
                )
        )
        self.sum_cart_list()
        self.page.update()

    #selecionar item do carrinho
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


    #remover do carrinho
    def remove_from_cart(self, e):
        if not self.selected_cart_control:
            build_snack(self.page,"Selecione um item do carrinho!")
            return

        self.cart_list.controls.remove(self.selected_cart_control)
        self.selected_cart_control = None
        self.selected_card_product = None
        self.sum_cart_list()
        self.page.update()

    # ================= SOMA TOTAL =================

    def sum_cart_list(self):
        cart_items = [item.data for item in self.cart_list.controls]
        total = calculate_total(cart_items)
        self.total_text.value = f"Total: {total:.2f}"


    # ============FINALIZAR COMPRA ===============

    def finalizar_compra(self, e):
        if len(self.cart_list.controls) == 0:
            build_snack(self.page,"O carrinho esta vazio!")
            return
        
        cart_items = [item.data for item in self.cart_list.controls]
        finalize_sale(cart_items)

        #limpa carrinho
        self.cart_list.controls.clear() 
        self.total_text.value = "Total: 0.00 "
        self.selected_cart_control = None
        self.selected_card_product = None

        build_snack(self.page,"Venda finalizada com sucesso!", ft.Colors.GREEN)
        self.page.update()

    # ================= BUILD ====================

    def build(self):
        self.page.controls.clear()
        self.page.bgcolor = ft.Colors.WHITE
        self.page.window.full_screen = True
        self.page.appbar = _appbar("Mini Market Flet")

        from views.history_view import Historico

        if not self.products_loaded:
            self.load_products()
            self.products_loaded = True

        navegacao = _navigation_history(lambda e: self.router.go("history", Historico))

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

                    style_product_list(self.product_list),

                    botao_padrao_home("ADICIONAR PRODUTO",self.add_to_cart, ButtonType.PRIMARY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12
            ),
            **card_padrao_home(),
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

                    style_cart_list(content=self.cart_list),

                    ft.Divider(height=15, color=ft.Colors.BLACK),

                    botao_padrao_home("REMOVER PRODUTO",self.remove_from_cart, ButtonType.SUCCESS),
                    botao_padrao_home("FINALIZAR COMPRA",self.finalizar_compra, ButtonType.DANGER),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12
            ),
            **card_padrao_home(),
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

