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
                       confirmed_rules
                       )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin_users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       username TEXT,
                       firstname TEXT,
                       lastname TEXT,
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
                "INSERT INTO users (user_id, username, firstname, lastname, created_at) VALUES (?, ?, ?, ?, ?)",
                (user.user_id, user.username, user.firstname, user.lastname, created_at)
            )
            self.con.commit() 
            
    def update_user_confirmed_rules(self, user_id, confirmed: bool = False):
        self.cursor.execute("""
                UPDATE users
                SET confirmed_rules = ?
                WHERE user_id = ?
            """, (str(confirmed), user_id))
        
        self.con.commit() 
        

        
        
          

        
    def close(self):
        self.con.close()
