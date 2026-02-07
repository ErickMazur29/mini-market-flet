import sqlite3
import os

nome_bd = "mercado.db"

def get_connection():
    conn = sqlite3.connect(nome_bd)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# TABELAS
def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER
                    )
            """)
        conn.commit()

        cursor.execute("""
            INSERT INTO produtos (nome, preco, quantidade) VALUES
            ('Arroz 5kg', '25.90', 50),
            ('Feijão 1kg', '8.50', 80),
            ('Macarrão', '4.20', 100),
            ('Açúcar 1kg', '4.80', 70),
            ('Óleo de Soja', '7.90', 60),
            ('Leite 1L', '4.50', 120),
            ('Café 500g', '14.90', 40),
            ('Farinha de Trigo 1kg', '6.30', 55),
            ('Biscoito', '3.50', 90),
            ('Refrigerante 2L', '8.99', 45)
        """)
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                total REAL NOT NULL)

        """)
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                id_venda INTEGER NOT NULL,
                preco REAL NOT NULL,
                    
                FOREIGN KEY (id_venda) REFERENCES vendas(id),
                FOREIGN KEY (id_produto) REFERENCES produtos(id)
                )
        """)
        conn.commit()


    
