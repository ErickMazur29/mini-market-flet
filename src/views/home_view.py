import flet as ft
from database.data import get_connection
from datetime import datetime

class Home:
    def __init__(self, page: ft.Page):
        self.page = page

        self.products_loaded = False
        self.selected_product = None #clicar na lista de produtos
        self.selected_product_control = None #controlador para ver se esta clicado ou nao
        self.selected_card_product = None #clicar na lista de compras
        self.selected_cart_control = None #controlador para ver se esta clicado ou nao

        self.total_text = ft.Text("Total: $0.00", size=18, weight="bold", color=ft.Colors.BLACK26)

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

        # Drawer de navegação
        self.page.drawer = ft.NavigationDrawer(
            on_change=self.navigate,
            controls=[
                ft.Container(height=50),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.INVENTORY, label="Produtos"
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.LOGOUT, label="Sair"
                ),
            ]
        )

    def _open_drawer(self, e):
        """Abre o menu lateral"""
        self.page.drawer.open = True
        self.page.update()

    def navigate(self, e):
        """Gerencia a navegação do menu"""
        index = e.control.selected_index

        # Fecha o drawer após selecionar
        self.page.drawer.open = False
        self.page.update()

        if index == 0:
            pass  # Dashboard (futuro)
        
        """
        elif index == 1:
            from .product_view import ProdutosView
            ProdutosView(self.page).build()

        elif index == 2:
            from .fornecedores_view import FornecedoresView
            FornecedoresView(self.page).build()

        elif index == 3:
            from .estoque_view import EstoqueView
            EstoqueView(self.page).build()

        elif index == 4:
            print("Logout (em desenvolvimento)")
        """

    # ================= PRODUTOS =================

    def load_products(self):
        self.product_list.controls.clear()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, preco FROM produtos")

            for product_id, name, price in cursor.fetchall():
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
        self.sum_card_list()
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
        self.sum_card_list()
        self.page.update()

    # ================= SOMA TOTAL =================

    def sum_card_list(self):
        total = 0

        for item in self.cart_list.controls:
            total = total + item.data["price"]

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
        
        total = 0

        for item in self.cart_list.controls:
            total = total + item.data["price"]

        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO vendas (data, total) VALUES (?,?)', (data_venda, total))
            id_venda = cursor.lastrowid

            for item in self.cart_list.controls:
                cursor.execute("""
                    INSERT INTO itens_venda (id_produto, id_venda, preco) VALUES (?,?,?)  """,
                    (
                        item.data["id"],
                        id_venda,
                        item.data["price"]
                    )
                )
            conn.commit()

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
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        if not self.products_loaded:
            self.load_products()
            self.products_loaded = True

        self.page.appbar = ft.AppBar(
            title=ft.Text("Mini Market", size=25, weight="bold"),
            leading=ft.IconButton(icon=ft.Icons.MENU, on_click=self._open_drawer),
        )

        styled_product_list = ft.Container(
            content=self.product_list,   
            width=400,
            height=300,
            padding=10,                
            margin=ft.margin.only(top=10, bottom=10),  
            bgcolor=ft.Colors.GREY_100, 
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300),

        )

        styled_cart_list = ft.Container(
            content=ft.Column(
                [
                    self.cart_list,
                    ft.Divider(height=15, color=ft.Colors.GREY),
                    self.total_text
                ]
            ),
            width=400,
            height=300,
            padding=10,
            border_radius=12,
            bgcolor=ft.Colors.GREY_100, 
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

        card_style = {
            "bgcolor": ft.Colors.WHITE,
            "padding": 30,
            "width": 420,
            "height": 650,
            "border_radius": 20,
            "shadow": ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        }


        #LAYOUT

        home_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Faça o pedido do cliente!",
                        size=24,
                        weight="bold",
                        color=ft.Colors.BLACK87
                    ),

                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),

                    styled_product_list,

                    ft.ElevatedButton(
                        text="ADICIONAR PRODUTO",
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
            **card_style,
            expand=1
        )

        cart_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Carrinho",
                        size=24,
                        weight="bold",
                        color=ft.Colors.BLACK87
                    ),
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),


                    styled_cart_list,
                    ft.Divider(height=15, color=ft.Colors.BLACK),
                    ft.ElevatedButton(
                        text="REMOVER PRODUTO",
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=self.remove_from_cart
                        
                    ),


                    ft.ElevatedButton(
                        text="FINALIZAR COMPRA",
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
            **card_style,
            expand=1
        )

        #RODAR OS DOIS CARDS

        juntar = ft.Row(
            controls=[
                home_card,
                cart_card
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20


            )
        self.page.add(juntar)
        self.page.update()
