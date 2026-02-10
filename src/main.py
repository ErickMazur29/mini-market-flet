import flet as ft
from views.auth_view import Login
from database.data import create_table

def main(page: ft.Page):
    create_table() #para criar as nossas tabelas no banco de dados
    
    page.title= "Sistema de Gestão de Estoque"

    login_view = Login(page) 
    login_view.build()

ft.run(main)