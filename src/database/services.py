#FAZER UMA VALIDAÇÃO PARA SABER SE A TABELA EXISTE ANTES DE INICIAR

from database.data import get_connection

def existe_historico_vendas():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendas")
        return cursor.fetchone()[0] > 0
