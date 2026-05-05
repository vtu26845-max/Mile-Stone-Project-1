# Relational Inventory Control and Stock Tracking System

A complete full-stack web application for managing inventory, tracking stock levels, and monitoring product movements. Built with Python Flask, SQLite, HTML5, CSS3, and JavaScript.

## 🚀 Features

### Authentication System
- User registration and login
- Session-based authentication
- Secure password hashing using SHA-256
- Logout functionality

### Dashboard
- Real-time statistics (total products, low stock alerts, inventory value)
- Recent activity logs
- Quick action buttons
- Low stock warnings

### Product Management
- Add new products with validation
- Edit existing products
- Delete products with confirmation
- View all products in a table format
- Search products by name
- Filter products by category

### Stock Tracking
- Increase stock levels
- Decrease stock levels
- Automatic inventory log updates
- Stock level indicators (normal, low)

### Inventory Logs
- Track all stock movements
- View change history (initial, increase, decrease)
- Timestamped entries

## 🛠️ Tech Stack

### Backend
- **Python Flask** - Web framework
- **SQLite** - Database
- **Flask-Session** - Session management

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with modern design
- **JavaScript** - Interactive functionality

## 📁 Project Structure

```
Relational Inventory Control and Stock Tracking System/
├── app.py                      # Main Flask application
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── backend/                    # Backend directory
├── frontend/                   # Frontend directory
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Dashboard page
│   ├── products.html          # Products list page
│   ├── add_product.html       # Add product form
│   ├── edit_product.html      # Edit product form
│   ├── stock_update.html      # Stock update form
│   └── logs.html              # Inventory logs page
└── static/                     # Static files
    ├── css/
    │   └── styles.css         # Main stylesheet
    └── js/
        └── script.js          # JavaScript functionality
```

## 📋 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password` - Hashed password
- `created_at` - Timestamp

### Products Table
- `id` - Primary key
- `name` - Product name
- `category` - Product category
- `price` - Product price
- `quantity` - Stock quantity
- `supplier` - Supplier name
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Inventory Logs Table
- `id` - Primary key
- `product_id` - Foreign key to products
- `change_type` - Type of change (INITIAL, INCREASE, DECREASE)
- `quantity` - Quantity changed
- `date` - Timestamp

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd "Relational Inventory Control and Stock Tracking System"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python init_db.py
```

This will create the SQLite database with all required tables and sample data.

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Login
- Use the default admin credentials or register a new account
- Navigate to the login page at `http://localhost:5000/login`

### 2. Dashboard
- View real-time statistics
- Check low stock alerts
- See recent activity
- Use quick action buttons

### 3. Add Product
- Click "Add Product" from the Products page
- Fill in the product details (name, category, price, quantity, supplier)
- Click "Add Product" to save

### 4. Manage Products
- View all products on the Products page
- Search by product name
- Filter by category
- Edit product details
- Delete products (with confirmation)

### 5. Update Stock
- Click the stock update button on any product
- Choose to increase or decrease stock
- Enter the quantity
- Changes are automatically logged

### 6. View Logs
- Access the Logs page to see all inventory movements
- Filter and sort through history

## 🎨 UI Features

- **Responsive Design** - Works on desktop and mobile devices
- **Modern UI** - Clean, professional interface
- **Gradient Colors** - Beautiful color schemes
- **Hover Effects** - Interactive elements
- **Flash Messages** - Success and error notifications
- **Form Validation** - Client and server-side validation
- **Table Styling** - Clean data presentation
- **Dashboard Cards** - Visual statistics display

## 🔐 Security Features

- Password hashing using SHA-256
- Session-based authentication
- Login required for protected routes
- Form validation
- SQL injection prevention (using parameterized queries)

## 📊 Sample Data

The database initialization includes:
- 1 default admin user
- 10 sample products across different categories
- Sample inventory logs

## 🔄 API Endpoints

The application includes REST API endpoints:

- `GET /api/products` - Get all products
- `GET /api/product/<id>` - Get specific product
- `GET /api/stats` - Get dashboard statistics

## 🐛 Troubleshooting

### Database Lock Error
If you encounter a database lock error, ensure the database file is not open in another application.

### Port Already in Use
If port 5000 is already in use, modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or another port
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📝 Customization

### Change Secret Key
Edit the secret key in `app.py` for production:
```python
app.secret_key = 'your-new-secret-key-here'
```

### Modify Database
Edit `init_db.py` to change the sample data or schema.

### Customize UI
Edit `static/css/styles.css` to change the visual design.

## 📄 License

This project is open source and available for educational purposes.

## 👥 Support

For issues or questions, please refer to the code comments or modify the application as needed.

## 🎯 Future Enhancements

Potential improvements:
- User roles and permissions
- Export data to CSV/Excel
- Barcode scanning
- Multi-location inventory
- Supplier management
- Purchase orders
- Sales tracking
- Reporting and analytics
- Email notifications for low stock

---

**Built with ❤️ using Python Flask**
