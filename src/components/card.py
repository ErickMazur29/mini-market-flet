import flet as ft

def card_padrao_login(content):
    return ft.Container(
        content = content,
        bgcolor = ft.Colors.WHITE,
        padding = 40,
        width = 400, 
        border_radius = 20,
        shadow = ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
    )

def card_padrao_home(content):
    return ft.Container(
        content = content,
        bgcolor = ft.Colors.WHITE,
        padding = 30,
        width = 350,
        height = 600,
        border_radius = 20,
        shadow = ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
    )

def cart_style():
    pass