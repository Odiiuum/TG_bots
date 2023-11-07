import sqlite3

connection = sqlite3.connect("db/database.db")
cursor = connection.cursor()

def create_tables():
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS account (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT NOT NULL,
        type TEXT NOT NULL,
        cred_limit REAL,
        curr_balance REAL NOT NULL,
        debt REAL
        )
      ''')
  
  connection.commit()

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT
        )
      ''')
  
  connection.commit()

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        comment TEXT,
        price REAL NOT NULL,
        from_account TEXT NOT NULL,
        to_account TEXT NOT NULL
        )
      ''')
  
  connection.commit()


connection.close()