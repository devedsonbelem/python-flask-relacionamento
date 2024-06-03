import sqlite3
import sys
import os
diretorio_raiz = 'c:\\Users\\edson\\app_python'
sys.path.append(os.path.abspath(diretorio_raiz)) 
from model.users import Users
from model.endereco import Endereco
import uuid


class Repositories:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS endereco (
                    endereco_id TEXT PRIMARY KEY,
                    logradouro TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    user_id TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')

    def add_user(self, user):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_id,name, email) VALUES (?, ?, ?)', (user.user_id,user.name, user.email))
            user.id_user = cursor.lastrowid
        return user.to_dict()

    def get_user_by_id(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return Users(user_id=row[0], name=row[1], email=row[2]) 

    def get_all_users(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            return [Users(*row) for row in rows]

    def add_endereco(self, endereco):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            endereco_ids = str(uuid.uuid4())
            cursor.execute('INSERT INTO endereco (endereco_id, logradouro, bairro, user_id) VALUES (?, ?, ?, ?)', ( endereco_ids ,  endereco.logradouro,  endereco.bairro, endereco.user_id))
            endereco.endereco_id = endereco_ids
        return endereco.to_dict()
    
    def get_endereco_by_id(self, endereco_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM endereco WHERE endereco_id = ?', (endereco_id,))
            row = cursor.fetchone()
            if row:
                return Endereco(endereco_id=row[0], logradouro=row[1], bairro=row[2], user_id=row[3])
    def get_all_enderecos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM endereco')
            rows = cursor.fetchall()
            return [Endereco(*row) for row in rows]

    def innerjoin(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT e.endereco_id, e.logradouro, e.bairro, e.user_id, u.name, u.email
            FROM endereco e
            INNER JOIN users u ON e.user_id = u.user_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            enderecos_com_usuarios = []
            for row in rows:
                endereco = {
                    "endereco_id": row[0],
                    "logradouro": row[1],
                    "bairro": row[2],
                    "user_id": row[3]
                }
                user = {
                    "user_id": row[3],
                    "name": row[4],
                    "email": row[5]
                }
                enderecos_com_usuarios.append({
                    "user": user,
                    "endereco": endereco
                    
                })
            
        return enderecos_com_usuarios
