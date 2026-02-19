from database.data import get_connection

def pegar_historico():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, total FROM vendas ORDER BY id DESC")
        vendas = cursor.fetchall()
        resultado = []

        for venda_id, venda_data, venda_total in vendas:
            cursor.execute("""
                SELECT p.nome, iv.preco FROM itens_venda as iv
                JOIN produtos p ON p.id = iv.id_produto
                WHERE iv.id_venda = ? 
                """, (venda_id,))
            
            produtos = cursor.fetchall()

            resultado.append({
                "data": venda_data,
                "total": venda_total,
                "produtos" : produtos
            })

        return resultado
            
