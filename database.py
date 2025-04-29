import sqlite3


def init_db():
    conn = sqlite3.connect("rxrewards.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS Customer
                 (CustomerID TEXT PRIMARY KEY, Name TEXT, Email TEXT, Phone TEXT, LoyaltyPoints INTEGER, TotalPurchase REAL)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS Product
                 (ProductName TEXT PRIMARY KEY, Category TEXT, Price REAL)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS Purchase
                 (PurchaseID TEXT PRIMARY KEY, CustomerID TEXT, ProductName TEXT, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID), FOREIGN KEY (ProductName) REFERENCES Product(ProductName))"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS PurchaseDetail
                 (PurchaseID TEXT, PurchaseDate TEXT, TotalAmount REAL, FOREIGN KEY (PurchaseID) REFERENCES Purchase(PurchaseID))"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS Discount
                 (DiscountID TEXT PRIMARY KEY, DiscountType TEXT, EligibilityCriteria TEXT, Percentage REAL)"""
    )
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect("rxrewards.db")
    return conn


def add_customer(customer_id, name, email, phone, loyalty_points, total_purchase):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?)",
        (customer_id, name, email, phone, loyalty_points, total_purchase),
    )
    conn.commit()
    conn.close()


def add_product(product_name, category, price):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO Product VALUES (?, ?, ?)", (product_name, category, price))
    conn.commit()
    conn.close()


def add_purchase(purchase_id, customer_id, product_name, purchase_date, total_amount):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO Purchase VALUES (?, ?, ?)",
        (purchase_id, customer_id, product_name),
    )
    c.execute(
        "INSERT INTO PurchaseDetail VALUES (?, ?, ?)",
        (purchase_id, purchase_date, total_amount),
    )
    conn.commit()
    conn.close()


def add_discount(discount_id, discount_type, eligibility_criteria, percentage):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO Discount VALUES (?, ?, ?, ?)",
        (discount_id, discount_type, eligibility_criteria, percentage),
    )
    conn.commit()
    conn.close()


def get_all_customers():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Customer")
    return c.fetchall()


def get_all_products():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Product")
    return c.fetchall()


def get_all_purchases():
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT p.PurchaseID, p.CustomerID, p.ProductName, pd.PurchaseDate, pd.TotalAmount FROM Purchase p JOIN PurchaseDetail pd ON p.PurchaseID = pd.PurchaseID"
    )
    return c.fetchall()


def get_all_discounts():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Discount")
    return c.fetchall()
