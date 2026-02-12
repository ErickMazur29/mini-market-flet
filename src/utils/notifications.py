import flet as ft

def build_snack(page, message, color=ft.Colors.RED):
    snack = ft.SnackBar(
        content=ft.Text(message, color=ft.Colors.WHITE),
        bgcolor=color,
        duration=1000,
        show_close_icon=True
    )
    page.overlay.clear()
    page.overlay.append(snack)
    snack.open = True
    page.update()
