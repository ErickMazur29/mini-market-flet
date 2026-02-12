import flet as ft

def _navigation(on_click):
    return ft.Column(
        [
            ft.IconButton(icon = ft.Icons.HOME),
            ft.IconButton(icon = ft.Icons.HISTORY, on_click=on_click)    
        ]
    )

def _appbar(title):
    title = ft.Text(title, size = 5, weight = "bold")