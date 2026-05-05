import sqlite3

def add_more_products():
    """Add more sample products to the existing database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Additional sample products
    more_products = [
        ('External Hard Drive 1TB', 'Electronics', 79.99, 60, 'TechSupplier Inc.'),
        ('Wireless Headphones', 'Electronics', 149.99, 45, 'AudioTech'),
        ('Bluetooth Speaker', 'Electronics', 59.99, 80, 'AudioTech'),
        ('Webcam HD', 'Electronics', 89.99, 35, 'TechSupplier Inc.'),
        ('Power Bank 20000mAh', 'Electronics', 39.99, 120, 'TechSupplier Inc.'),
        ('USB Hub 7-Port', 'Electronics', 24.99, 90, 'CableWorld'),
        ('HDMI Cable 6ft', 'Electronics', 9.99, 200, 'CableWorld'),
        ('Standing Desk', 'Furniture', 399.99, 15, 'Furniture Plus'),
        ('Bookshelf', 'Furniture', 149.99, 25, 'Furniture Plus'),
        ('File Cabinet', 'Furniture', 129.99, 20, 'Furniture Plus'),
        ('Ergonomic Mouse Pad', 'Furniture', 19.99, 100, 'Furniture Plus'),
        ('Desk Organizer', 'Stationery', 29.99, 85, 'PaperGoods Co.'),
        ('Highlighter Set', 'Stationery', 8.99, 180, 'PaperGoods Co.'),
        ('Binder 3-inch', 'Stationery', 6.99, 150, 'PaperGoods Co.'),
        ('Printer Paper (500 sheets)', 'Stationery', 12.99, 200, 'PaperGoods Co.'),
        ('Scissors', 'Stationery', 4.99, 120, 'PaperGoods Co.'),
        ('Tape Dispenser', 'Stationery', 7.99, 95, 'PaperGoods Co.'),
        ('Whiteboard Markers', 'Stationery', 11.99, 70, 'PaperGoods Co.'),
        ('Calculator', 'Electronics', 14.99, 65, 'TechSupplier Inc.'),
        ('Laptop Stand', 'Furniture', 49.99, 40, 'Furniture Plus'),
        ('Monitor Arm', 'Furniture', 79.99, 30, 'Furniture Plus'),
        ('Cable Management Kit', 'Electronics', 19.99, 110, 'CableWorld'),
        ('Screen Cleaning Kit', 'Electronics', 12.99, 140, 'TechSupplier Inc.'),
        ('Wireless Charger', 'Electronics', 34.99, 75, 'TechSupplier Inc.'),
        ('Tablet Stand', 'Electronics', 29.99, 55, 'TechSupplier Inc.'),
        ('Desk Mat XL', 'Furniture', 24.99, 88, 'Furniture Plus'),
        ('Pencil Case', 'Stationery', 9.99, 160, 'PaperGoods Co.'),
        ('Correction Tape', 'Stationery', 3.99, 220, 'PaperGoods Co.'),
        ('Index Cards (100 pack)', 'Stationery', 5.99, 130, 'PaperGoods Co.'),
        ('Glue Stick', 'Stationery', 2.99, 250, 'PaperGoods Co.'),
        ('USB-C Hub Multiport', 'Electronics', 44.99, 50, 'CableWorld'),
        ('Laptop Sleeve 15"', 'Electronics', 29.99, 60, 'TechSupplier Inc.'),
        ('Wireless Keyboard & Mouse Combo', 'Electronics', 59.99, 70, 'TechSupplier Inc.'),
        ('Desk Fan', 'Furniture', 34.99, 45, 'Furniture Plus'),
        ('LED Desk Lamp', 'Furniture', 39.99, 55, 'Furniture Plus'),
        ('Drawer Organizer', 'Furniture', 24.99, 40, 'Furniture Plus'),
        ('Post-it Notes (3 pack)', 'Stationery', 7.99, 190, 'PaperGoods Co.'),
        ('Paper Clips (500 count)', 'Stationery', 3.99, 280, 'PaperGoods Co.'),
        ('Rubber Bands (250 count)', 'Stationery', 2.99, 300, 'PaperGoods Co.'),
        ('Envelope A4 (100 pack)', 'Stationery', 8.99, 120, 'PaperGoods Co.'),
        ('Staples (1000 count)', 'Stationery', 4.99, 200, 'PaperGoods Co.'),
        ('Hole Punch', 'Stationery', 12.99, 60, 'PaperGoods Co.'),
        ('Ruler 12"', 'Stationery', 2.49, 180, 'PaperGoods Co.'),
        ('Protractor', 'Stationery', 1.99, 150, 'PaperGoods Co.'),
        ('Compass Set', 'Stationery', 5.99, 80, 'PaperGoods Co.'),
        ('Sketchbook A4', 'Stationery', 14.99, 70, 'PaperGoods Co.'),
        ('Colored Pencils (24 pack)', 'Stationery', 9.99, 95, 'PaperGoods Co.'),
        ('Marker Set (12 colors)', 'Stationery', 15.99, 65, 'PaperGoods Co.'),
        ('Dry Erase Board Small', 'Stationery', 19.99, 35, 'PaperGoods Co.')
    ]
    
    added_count = 0
    for product in more_products:
        try:
            cursor.execute('''
                INSERT INTO products (name, category, price, quantity, supplier)
                VALUES (?, ?, ?, ?, ?)
            ''', product)
            product_id = cursor.lastrowid
            
            # Log initial inventory
            cursor.execute('''
                INSERT INTO inventory_logs (product_id, change_type, quantity)
                VALUES (?, 'INITIAL', ?)
            ''', (product_id, product[3]))
            
            added_count += 1
            print(f"Added: {product[0]}")
        except sqlite3.IntegrityError:
            print(f"Skipped (already exists): {product[0]}")
    
    conn.commit()
    conn.close()
    
    print(f"\nSuccessfully added {added_count} new products to the database!")

if __name__ == '__main__':
    add_more_products()
