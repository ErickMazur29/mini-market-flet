import flet as ft
from router import Router
from views.login_view import Login
from database.data import create_table

def main(page: ft.Page):
    create_table()
    router = Router(page)
    router.go("login", Login)

ft.app(target=main)
