import flet as ft
from database.data import get_connection

def get_all_products():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(" SELECT id, nome, preco FROM produtos")
        result = cursor.fetchall()
        return result