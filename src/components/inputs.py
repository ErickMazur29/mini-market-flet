import flet as ft

def login_field(label, password=False):
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        color=ft.Colors.BLACK
    )