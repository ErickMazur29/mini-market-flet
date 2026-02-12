import flet as ft
from database.data import get_connection
from datetime import datetime


def existe_historico_vendas():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendas")
        return cursor.fetchone()[0] > 0
    

def finalize_sale(cart_items):
    total = sum(item["price"] for item in cart_items)
    data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO vendas (data, total) VALUES (?,?)', (data_venda, total))
        id_venda = cursor.lastrowid

        for item in cart_items:
            cursor.execute("""
                INSERT INTO itens_venda (id_produto, id_venda, preco) VALUES (?,?,?)  """,
                (item["id"], id_venda, item["price"])
            )
        conn.commit()