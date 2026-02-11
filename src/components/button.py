import flet as ft

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

def botao_padrao_home(text, on_click, colors):
    return ft.Button(
        text,
        width = 300,
        height = 45,
        style = ft.ButtonStyle(
            bgcolor = colors,
            color = ft.Colors.WHITE,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=on_click
    )