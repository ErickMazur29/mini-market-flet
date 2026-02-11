import flet as ft
from database.data import get_connection

class Login:
    def __init__(self, page, router):
        self.page = page
        self.router = router

        self.username = ft.TextField(label="Usuario", color=ft.Colors.BLACK)
        self.password = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.BLACK)

    def build(self):
        self.page.bgcolor = ft.Colors.WHITE
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.maximized = True

        self.page.appbar = ft.AppBar(title=ft.Text("Mini Market", size=25, weight="bold"),)

        from views.register_view import Register
        

        login_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=50, color=ft.Colors.BLUE),
                    ft.Text("Bem-vindo", size=30, weight='bold', color=ft.Colors.BLACK_87),
                    ft.Text("Acesse sua conta para continuar", color=ft.Colors.BLACK_54),
                    
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Espaçador
                    
                    self.username,
                    self.password,
                    
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    ft.Button(
                        "ENTRAR NO SISTEMA",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                        ),
                        width=300,
                        height=50,
                        on_click=self.login_entrada
                    ),
                    
                    ft.TextButton(
                        content=ft.Text("Não possui cadastro? Cadastre-se agora!", size=12),
                        on_click= lambda e:self.router.go("register", Register)
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=40,
            width=400, 
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
            ),
        )
        self.page.controls.clear()
        self.page.add(login_card)
        self.page.update()

        #NOTIFCAÇÕES

    def mostrar_notificacao(self, mensagem, cor=ft.Colors.RED):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE),
            bgcolor=cor,
            duration=1000,
            show_close_icon=True
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

        #ENTRADA
        
    def login_entrada(self, e):
        usuario = self.username.value.strip()
        senha = self.password.value.strip()

        if not usuario or not senha:
            # Chamada da notificação de erro
            self.mostrar_notificacao("Preencha todos os campos!")
            return
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password FROM usuarios WHERE user_name = ?', (usuario,)
            )
            resultado = cursor.fetchone()

            if resultado is None:
                self.mostrar_notificacao("Usuario nao cadastrado!")
                self.password.value = ""
                self.page.update()
                return
            
            senha_existente = resultado[0]

            if senha == senha_existente:
                from views.home_view import Home
                self.router.go("home", Home)
                self.mostrar_notificacao("Login realizado com sucesso!", ft.Colors.GREEN)

            else:
                self.mostrar_notificacao("Senha Incorreta!")
                self.password.value = ""
                self.page.update()
