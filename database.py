# database.py
import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS brands
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, brand_id INTEGER, photo_path TEXT,
                  FOREIGN KEY(category_id) REFERENCES categories(id),
                  FOREIGN KEY(brand_id) REFERENCES brands(id))''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
              (username, email, hashed))
    conn.commit()
    conn.close()

def verify_user(email, password):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False

def add_category(name):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def add_brand(name):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO brands (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def add_product(name, category_id, brand_id, photo_path):
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, category_id, brand_id, photo_path) VALUES (?, ?, ?, ?)',
              (name, category_id, brand_id, photo_path))
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM categories')
    categories = c.fetchall()
    conn.close()
    return categories

def get_brands():
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM brands')
    brands = c.fetchall()
    conn.close()
    return brands

def get_products():
    conn = sqlite3.connect('tienda.db')
    c = conn.cursor()
    c.execute('''SELECT p.id, p.name, c.name, b.name, p.photo_path
                 FROM products p
                 JOIN categories c ON p.category_id = c.id
                 JOIN brands b ON p.brand_id = b.id''')
    products = c.fetchall()
    conn.close()
    return products