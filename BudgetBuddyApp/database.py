import sqlite3
import os

def create_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'budgetbuddy.db')
    conn = sqlite3.connect(db_path)
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        due_date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_transaction(user_id, date, category, description, amount):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO transactions (user_id, date, category, description, amount) VALUES (?, ?, ?, ?, ?)',
              (user_id, date, category, description, amount))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions

def add_bill(user_id, due_date, category, description, amount):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO bills (user_id, due_date, category, description, amount) VALUES (?, ?, ?, ?, ?)',
              (user_id, due_date, category, description, amount))
    conn.commit()
    conn.close()

def get_bills(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM bills WHERE user_id = ?', (user_id,))
    bills = c.fetchall()
    conn.close()
    return bills

# Panggil fungsi create_tables untuk membuat tabel saat awal
create_tables()
