import sqlite3
from datetime import datetime
import hashlib

def init_database():
    """Initialize the SQLite database with all required tables and sample data."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Inventory Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            change_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Create a default admin user (password: admin123)
    hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', ('admin', hashed_password))
        print("Default admin user created (username: admin, password: admin123)")
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    
    # Insert sample products
    sample_products = [
        ('Laptop', 'Electronics', 999.99, 50, 'TechSupplier Inc.'),
        ('Wireless Mouse', 'Electronics', 29.99, 200, 'TechSupplier Inc.'),
        ('USB-C Cable', 'Electronics', 15.99, 300, 'CableWorld'),
        ('Office Chair', 'Furniture', 199.99, 30, 'Furniture Plus'),
        ('Desk Lamp', 'Furniture', 45.99, 75, 'Furniture Plus'),
        ('Notebook A4', 'Stationery', 5.99, 500, 'PaperGoods Co.'),
        ('Ballpoint Pen', 'Stationery', 1.99, 1000, 'PaperGoods Co.'),
        ('Stapler', 'Stationery', 12.99, 150, 'PaperGoods Co.'),
        ('Monitor 24"', 'Electronics', 249.99, 40, 'TechSupplier Inc.'),
        ('Keyboard', 'Electronics', 79.99, 120, 'TechSupplier Inc.')
    ]
    
    for product in sample_products:
        try:
            cursor.execute('''
                INSERT INTO products (name, category, price, quantity, supplier)
                VALUES (?, ?, ?, ?, ?)
            ''', product)
        except sqlite3.IntegrityError:
            pass
    
    # Insert sample inventory logs
    cursor.execute('''
        INSERT INTO inventory_logs (product_id, change_type, quantity)
        VALUES (1, 'INITIAL', 50)
    ''')
    cursor.execute('''
        INSERT INTO inventory_logs (product_id, change_type, quantity)
        VALUES (2, 'INITIAL', 200)
    ''')
    cursor.execute('''
        INSERT INTO inventory_logs (product_id, change_type, quantity)
        VALUES (1, 'RESTOCK', 20)
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data!")

if __name__ == '__main__':
    init_database()
