from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['SESSION_TYPE'] = 'filesystem'

DATABASE = 'inventory.db'

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorator to require login for certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Authentication Routes ====================

@app.route('/')
def index():
    """Redirect to login or dashboard based on authentication status."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and hashlib.sha256(password.encode()).hexdigest() == user['password']:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                        (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ==================== Dashboard Route ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Display dashboard with statistics."""
    conn = get_db_connection()
    
    # Total products
    total_products = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']
    
    # Low stock alert (products with quantity < 20)
    low_stock = conn.execute('SELECT COUNT(*) as count FROM products WHERE quantity < 20').fetchone()['count']
    
    # Total inventory value
    total_value = conn.execute('SELECT SUM(price * quantity) as total FROM products').fetchone()['total'] or 0
    
    # Recent inventory logs
    recent_logs = conn.execute('''
        SELECT il.*, p.name as product_name 
        FROM inventory_logs il
        JOIN products p ON il.product_id = p.id
        ORDER BY il.date DESC
        LIMIT 10
    ''').fetchall()
    
    # Low stock products
    low_stock_products = conn.execute('''
        SELECT * FROM products WHERE quantity < 20
        ORDER BY quantity ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                          total_products=total_products,
                          low_stock=low_stock,
                          total_value=total_value,
                          recent_logs=recent_logs,
                          low_stock_products=low_stock_products)

# ==================== Product Management Routes ====================

@app.route('/products')
@login_required
def products():
    """Display all products with search and filter options."""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY name'
    
    products = conn.execute(query, params).fetchall()
    
    # Get unique categories for filter dropdown
    categories = conn.execute('SELECT DISTINCT category FROM products ORDER BY category').fetchall()
    
    conn.close()
    
    return render_template('products.html', 
                          products=products, 
                          categories=categories,
                          search=search,
                          selected_category=category)

@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product."""
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        supplier = request.form['supplier']
        
        if not name or not category or not supplier:
            flash('All fields are required.', 'error')
            return render_template('add_product.html')
        
        if price <= 0 or quantity < 0:
            flash('Price must be positive and quantity cannot be negative.', 'error')
            return render_template('add_product.html')
        
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO products (name, category, price, quantity, supplier)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, price, quantity, supplier))
        product_id = cursor.lastrowid
        conn.commit()
        
        # Log initial inventory
        conn.execute('''
            INSERT INTO inventory_logs (product_id, change_type, quantity)
            VALUES (?, 'INITIAL', ?)
        ''', (product_id, quantity))
        conn.commit()
        conn.close()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edit an existing product."""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        supplier = request.form['supplier']
        
        if not name or not category or not supplier:
            flash('All fields are required.', 'error')
            conn.close()
            return render_template('edit_product.html', product=product)
        
        if price <= 0 or quantity < 0:
            flash('Price must be positive and quantity cannot be negative.', 'error')
            conn.close()
            return render_template('edit_product.html', product=product)
        
        old_quantity = product['quantity']
        quantity_diff = quantity - old_quantity
        
        conn.execute('''
            UPDATE products 
            SET name = ?, category = ?, price = ?, quantity = ?, supplier = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, category, price, quantity, supplier, product_id))
        
        # Log quantity change if there's a difference
        if quantity_diff != 0:
            change_type = 'INCREASE' if quantity_diff > 0 else 'DECREASE'
            conn.execute('''
                INSERT INTO inventory_logs (product_id, change_type, quantity)
                VALUES (?, ?, ?)
            ''', (product_id, change_type, abs(quantity_diff)))
        
        conn.commit()
        conn.close()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a product."""
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory_logs WHERE product_id = ?', (product_id,))
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# ==================== Stock Management Routes ====================

@app.route('/stock/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_stock(product_id):
    """Update stock for a product."""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        conn.close()
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        change_type = request.form['change_type']
        quantity = int(request.form['quantity'])
        
        if quantity <= 0:
            flash('Quantity must be positive.', 'error')
            conn.close()
            return render_template('stock_update.html', product=product)
        
        new_quantity = product['quantity']
        
        if change_type == 'increase':
            new_quantity += quantity
            conn.execute('''
                UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
            ''', (new_quantity, product_id))
            conn.execute('''
                INSERT INTO inventory_logs (product_id, change_type, quantity)
                VALUES (?, 'INCREASE', ?)
            ''', (product_id, quantity))
        elif change_type == 'decrease':
            if quantity > product['quantity']:
                flash('Cannot decrease stock below zero.', 'error')
                conn.close()
                return render_template('stock_update.html', product=product)
            new_quantity -= quantity
            conn.execute('''
                UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
            ''', (new_quantity, product_id))
            conn.execute('''
                INSERT INTO inventory_logs (product_id, change_type, quantity)
                VALUES (?, 'DECREASE', ?)
            ''', (product_id, quantity))
        
        conn.commit()
        conn.close()
        
        flash(f'Stock updated successfully! New quantity: {new_quantity}', 'success')
        return redirect(url_for('products'))
    
    conn.close()
    return render_template('stock_update.html', product=product)

@app.route('/logs')
@login_required
def inventory_logs():
    """Display inventory logs."""
    conn = get_db_connection()
    logs = conn.execute('''
        SELECT il.*, p.name as product_name 
        FROM inventory_logs il
        JOIN products p ON il.product_id = p.id
        ORDER BY il.date DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

# ==================== API Routes ====================

@app.route('/api/products', methods=['GET'])
@login_required
def api_products():
    """API endpoint to get all products."""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY name').fetchall()
    conn.close()
    
    return jsonify([dict(product) for product in products])

@app.route('/api/product/<int:product_id>', methods=['GET'])
@login_required
def api_product(product_id):
    """API endpoint to get a specific product."""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    """API endpoint to get dashboard statistics."""
    conn = get_db_connection()
    total_products = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']
    low_stock = conn.execute('SELECT COUNT(*) as count FROM products WHERE quantity < 20').fetchone()['count']
    total_value = conn.execute('SELECT SUM(price * quantity) as total FROM products').fetchone()['total'] or 0
    conn.close()
    
    return jsonify({
        'total_products': total_products,
        'low_stock': low_stock,
        'total_value': total_value
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
