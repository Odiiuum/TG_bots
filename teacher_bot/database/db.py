import sqlite3
from datetime import datetime

from config_reader import config

class Database:
    def __init__(self, db_path="data.db"):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()

    def create_init_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE,
                        username TEXT,
                        firstname TEXT,
                        lastname TEXT,
                        created_at TEXT,
                        confirmed_rules TEXT,
                        current_state TEXT
                        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        firstname TEXT,
                        lastname TEXT,
                        created_at TEXT
                        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS rules(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        created_at TEXT
                        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS compliments_female(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT,
                        text TEXT,
                        created_at TEXT
                        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS compliments_male(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT,
                        text TEXT,
                        created_at TEXT
                        )""")
        
        user_id = config.admin_uid
        username = config.admin_username
        firstname  = config.admin_firstname
        lastname = config.admin_lastname
        
        self.cursor.execute("SELECT COUNT(*) FROM admin_users WHERE user_id = ?", (user_id, ))
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            self.cursor.execute(
                "INSERT INTO admin_users (user_id, username, firstname, lastname, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, firstname, lastname, created_at)
            )
            self.con.commit()
        
        self.con.commit()
    
    def get_admin_users(self):
        self.cursor.execute("SELECT * FROM admin_users")
        return self.cursor.fetchall()
    
    def add_user(self, user):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user.user_id,))
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            self.cursor.execute(
                "INSERT INTO users (user_id, username, firstname, lastname, created_at, confirmed_rules) VALUES (?, ?, ?, ?, ?, ?)",
                (user.user_id, user.username, user.firstname, user.lastname, created_at, "False")
            )
            self.con.commit() 
            
    def update_user_confirmed_rules(self, user_id, confirmed):
        self.cursor.execute("""
                UPDATE users
                SET confirmed_rules = ?
                WHERE user_id = ?
            """, (str(confirmed), user_id))
        
        self.con.commit() 
        
    def get_user_confirmed_rules(self, user_id: int):
        self.cursor.execute("SELECT confirmed_rules FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()[0]
        return result
    
    def get_last_rule(self):
        self.cursor.execute("SELECT * FROM rules ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()[1]
        return result
        
    def get_compliments_female(self):
        self.cursor.execute("SELECT * FROM compliments_female")
        count = self.cursor.fetchall()
        return count
    
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    
    def update_user_state(self, user_id: int, current_state):
        self.cursor.execute("""
                            UPDATE users
                            SET current_state = ?
                            WHERE user_id = ?
                            """, (current_state, user_id))
    
        self.con.commit() 
    
          

        
    def close(self):
        self.con.close()
