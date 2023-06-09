import sqlite3

from entity.User import User

class UserRepository:

    def set_up_users_repository(self):
        # criação do banco de dados e tabela para usuários
        self.conn = sqlite3.connect('event_click.db')
        def trace_callback(query):
            print(query)
        self.conn.set_trace_callback(trace_callback)
        self.c = self.conn.cursor()
        # self.c.execute('''DROP TABLE users''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                (id TEXT PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, is_organizer INTEGER)''')
        
    def insert_user(self, id, name, email, password, is_organizer):
        self.c.execute("INSERT INTO users VALUES (?,?,?,?,?)", (id, name, email, password, is_organizer))
        self.conn.commit()
        
    def get_user_by_email(self, email):
        self.c.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.c.fetchone()
        
    def get_user_by_id(self, id):
        self.c.execute("SELECT * FROM users WHERE id=?", (id,))
        return self.c.fetchone()
    
    def update_user(self, user_id, is_organizer):
        self.c.execute("UPDATE users SET is_organizer = ? WHERE id = ?", (is_organizer, user_id))
        self.conn.commit()