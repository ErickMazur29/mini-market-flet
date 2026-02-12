import flet as ft
from utils.constants import ButtonType

def botao_primario_login(text, on_click):
    return ft.Button(
        text,
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius=10),
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.BLUE,
        ),
        width=300,
        height=50,
        on_click = on_click
    )



def botao_padrao_home(text, on_click, tipo: ButtonType):
    cores = {
        ButtonType.PRIMARY: ft.Colors.BLUE,
        ButtonType.SUCCESS: ft.Colors.GREEN,
        ButtonType.DANGER: ft.Colors.RED,
        ButtonType.WARNING: ft.Colors.ORANGE,
    }

    return ft.Button(
        text=text,
        width=300,
        height=45,
        style=ft.ButtonStyle(
            bgcolor=cores[tipo],
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=on_click,
    )
