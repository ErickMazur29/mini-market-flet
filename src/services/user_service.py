from database.data import get_connection
from utils.security import hash_password
import sqlite3

def login_user(usuario, senha):
    user = usuario
    password_hash = hash_password(senha)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM usuarios WHERE user_name = ?', (user,))
        result = cursor.fetchone()
        
        if not result:
            return False, "Usuario não encontrado"
        
        senha_salva = result[0]
        
        if senha_salva != password_hash:
            return False, "Senha incorreta"
        
    return True, "Login realizado com sucesso!"

    
def crate_account(user, senha):
    passoword_hash = hash_password(senha)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (user_name, password) VALUES (?, ?)',(user, passoword_hash))
            conn.commit()

        return True, 'Usuario cadastrado com sucesso'
    
    except sqlite3.IntegrityError:
        return False, "Usuario ja existente"
    
