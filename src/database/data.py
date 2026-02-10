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
                ('Arroz 5kg', 24.90, 50),
                ('Feijão Carioca 1kg', 7.50, 100),
                ('Azeite de Oliva 500ml', 35.00, 30),
                ('Café Torrado 500g', 18.90, 80),
                ('Açúcar Refinado 1kg', 4.20, 200),
                ('Macarrão Espaguete 500g', 3.80, 150),
                ('Óleo de Soja 900ml', 6.50, 120),
                ('Leite Integral 1L', 4.90, 300),
                ('Farinha de Trigo 1kg', 5.10, 90),
                ('Sal Refinado 1kg', 2.50, 100),
                ('Molho de Tomate 300g', 2.90, 200),
                ('Biscoito Recheado', 2.50, 150),
                ('Sabão em Pó 1kg', 12.00, 60),
                ('Detergente Líquido', 1.99, 250),
                ('Desinfetante 1L', 5.50, 70),
                ('Amaciante 2L', 15.00, 40),
                ('Papel Higiênico 4un', 6.00, 100),
                ('Shampoo 400ml', 12.50, 50),
                ('Sabonete Barra', 1.50, 400),
                ('Creme Dental', 3.20, 180),
                ('Alface Americana', 3.00, 40),
                ('Tomate Longa Vida kg', 6.00, 60),
                ('Banana Prata kg', 4.50, 80),
                ('Maçã Gala kg', 7.00, 70),
                ('Batata Inglesa kg', 5.00, 100),
                ('Cebola kg', 4.00, 120),
                ('Peito de Frango kg', 16.00, 50),
                ('Carne Moída kg', 25.00, 40),
                ('Pão de Forma', 5.50, 60),
                ('Iogurte Natural 170g', 2.80, 100);
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

        cursor.execute("""
            DELETE FROM produtos WHERE id >30
        """)
        conn.commit()


    
