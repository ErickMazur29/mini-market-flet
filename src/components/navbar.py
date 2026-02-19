import flet as ft

def _navigation_history(on_click):
    return ft.Column(
        [
            ft.IconButton(icon = ft.Icons.HISTORY, on_click=on_click)    
        ]
    )

def _navigation_home(on_click):
    return ft.Column(
        [
            ft.IconButton(icon = ft.Icons.HOME, on_click=on_click)    
        ]
    )

def _appbar(title):
    return ft.AppBar(
        title = ft.Text(title, size=25, weight='bold')
    )