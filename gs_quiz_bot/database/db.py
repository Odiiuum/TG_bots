import sqlite3
from handlers import init_questions
from datetime import datetime

from config_reader import config

class Database:
    def __init__(self, db_path="data.db"):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()

    def check_init_table(self, table, init_data):
        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = self.cursor.fetchone()[0]
        if count == 0:
            for question in init_data:
                self.cursor.execute(f"INSERT INTO {table} (question) VALUES (?)", (question,))

    def create_init_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tg_id INTEGER,
                       username TEXT,
                       firstname TEXT,
                       lastname TEXT,
                       created_at TEXT
                       )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tg_id INTEGER,
                       username TEXT,
                       firstname TEXT,
                       lastname TEXT,
                       created_at TEXT
                       )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS questions_theory(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT
                       )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS questions_practice(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT
                       )""")
        
        self.check_init_table("questions_theory", init_questions.theory)
        self.check_init_table("questions_practice", init_questions.practice)
        
        user_id = config.admin_uid
        username = config.admin_username
        firstname  = config.admin_firstname
        lastname = config.admin_lastname
        
        self.cursor.execute("SELECT COUNT(*) FROM admin_users WHERE username = ?", (username,))
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            self.cursor.execute(
                "INSERT INTO admin_users (tg_id, username, firstname, lastname, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, firstname, lastname, created_at)
            )
            self.con.commit()
        
        self.con.commit()

    def get_questions(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()
    
    def get_admin_users(self):
        self.cursor.execute(f"SELECT * FROM admin_users")
        return self.cursor.fetchall()
    
    def add_user(self, user):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (user.username,))
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            self.cursor.execute(
                "INSERT INTO users (tg_id, username, firstname, lastname, created_at) VALUES (?, ?, ?, ?, ?)",
                (user.tg_id, user.username, user.firstname, user.lastname, created_at)
            )
            self.con.commit()
        
    def close(self):
        self.con.close()
