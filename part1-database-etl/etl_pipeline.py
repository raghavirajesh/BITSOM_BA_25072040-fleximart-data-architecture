import pandas as pd
import re

# -----------------------
# Helper Functions
# -----------------------

def standardize_phone(phone):
    if pd.isna(phone):
        return None
    phone = re.sub(r'\D', '', str(phone))  # remove non-digits
    phone = phone[-10:]  # keep last 10 digits
    return "+91" + phone


def standardize_date(date):
    return pd.to_datetime(date, errors="coerce").dt.strftime("%Y-%m-%d")


def clean_category(cat):
    if pd.isna(cat):
        return None
    cat = cat.strip().lower()
    if cat == "electronics":
        return "Electronics"
    elif cat == "fashion":
        return "Fashion"
    elif cat == "groceries":
        return "Groceries"
    return cat.capitalize()


# -----------------------
# EXTRACT
# -----------------------

customers = pd.read_csv("data/customers_raw.csv")
products = pd.read_csv("data/products_raw.csv")
sales = pd.read_csv("data/sales_raw.csv")


print("Data Loaded Successfully")

# -----------------------
# TRANSFORM: CUSTOMERS
# -----------------------

# Remove duplicates
customers = customers.drop_duplicates(subset="customer_id")
customers.drop_duplicates(subset="email", inplace=True)
customers.dropna(subset=["email"], inplace=True) #Used drop here as email is unique and primary contact source.

# Handle missing emails
customers["email"] = customers.apply(
    lambda x: x["email"] if pd.notna(x["email"]) else f"unknown_{x['customer_id']}@example.com",
    axis=1
)

# Fix phone numbers
def standardize_phone(phone):
    phone = str(phone).strip().lower()

    # Handle missing values AFTER astype(str)
    if phone in ["nan", "none", ""]:
        return None

    # Remove everything except digits
    phone = re.sub(r"\D", "", phone)

    # Keep last 10 digits (removes 91, 0, etc.)
    if len(phone) > 10:
        phone = phone[-10:]

    return "+91" + phone


customers["phone"] = customers["phone"].astype(str)
customers["phone"] = customers["phone"].apply(standardize_phone)
#print(customers[["customer_id", "phone"]])

# Fix city casing
customers["city"] = customers["city"].str.strip().str.title()

# Fix date formats
def parse_mixed_date(date):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(date, format=fmt)
        except (ValueError, TypeError):
            pass
    return pd.NaT


customers["registration_date"] = (
    customers["registration_date"]
    .astype(str)
    .str.strip()
    .apply(parse_mixed_date)
)

customers["registration_date"] = customers["registration_date"].dt.date

# Convert NaT → None for SQL
customers["registration_date"] = customers["registration_date"].where(
    customers["registration_date"].notna(), None
)

#print(customers.head(25))

# -----------------------
# TRANSFORM: PRODUCTS
# -----------------------

# Strip extra spaces in product names
products["product_name"] = products["product_name"].str.strip()

# Fix categories
products["category"] = products["category"].apply(clean_category)

# Fill missing prices with median because if we give Zero, it might mean that the product is for free.
price_median = products["price"].median()
products["price"] = products["price"].fillna(price_median)

# Fill missing stock with 0
products["stock_quantity"] = products["stock_quantity"].fillna(0).astype(int)

#print(products.head(20))

# -----------------------
# TRANSFORM: SALES
# -----------------------

# Remove duplicate transactions
sales = sales.drop_duplicates(subset="transaction_id")

# Drop rows with missing customer_id or product_id
sales = sales.dropna(subset=["customer_id", "product_id"])

# Fix date formats
# ---------- SALES DATE CLEANING ----------

def parse_mixed_date(date):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y"):
        try:
            return pd.to_datetime(date, format=fmt)
        except (ValueError, TypeError):
            pass
    return pd.NaT


sales["transaction_date"] = (
    sales["transaction_date"]
    .astype(str)
    .str.strip()
    .apply(parse_mixed_date)
)

# Convert NaT → None for SQL
sales["transaction_date"] = sales["transaction_date"].where(
    sales["transaction_date"].notna(), None
)


sales["transaction_date"] = sales["transaction_date"].dt.date

#print(sales.head(40))

# -----------------------
# SAVE CLEAN FILES
# -----------------------

customers.to_csv("customers_clean.csv", index=False)
products.to_csv("products_clean.csv", index=False)
sales.to_csv("sales_clean.csv", index=False)

customers_raw = pd.read_csv("data/customers_raw.csv")
customers_clean = pd.read_csv("customers_clean.csv")

customers_total = len(customers_raw)
customers_duplicates = customers_raw.duplicated(subset="customer_id").sum()
customers_missing = customers_raw.isna().sum().sum()
customers_loaded = len(customers)

products_raw = pd.read_csv("data/products_raw.csv")
products_clean = pd.read_csv("products_clean.csv")

products_total = len(products_raw)
products_duplicates = 0  # none specified
products_missing = products_raw.isna().sum().sum()
products_loaded = len(products)

sales_raw = pd.read_csv("data/sales_raw.csv")
sales_clean = pd.read_csv("sales_clean.csv")

sales_total = len(sales_raw)
sales_duplicates = sales_raw.duplicated(subset="transaction_id").sum()
sales_missing = sales_raw.isna().sum().sum()
sales_loaded = len(sales)

with open("data_quality_report.txt", "w") as f:
    f.write("DATA QUALITY REPORT\n")
    f.write("===================\n\n")

    f.write("CUSTOMERS\n")
    f.write(f"Records processed: {customers_total}\n")
    f.write(f"Duplicates removed: {customers_duplicates}\n")
    f.write(f"Missing values handled: {customers_missing}\n")
    f.write(f"Records loaded successfully: {customers_loaded}\n\n")

    f.write("PRODUCTS\n")
    f.write(f"Records processed: {products_total}\n")
    f.write(f"Duplicates removed: {products_duplicates}\n")
    f.write(f"Missing values handled: {products_missing}\n")
    f.write(f"Records loaded successfully: {products_loaded}\n\n")

    f.write("SALES\n")
    f.write(f"Records processed: {sales_total}\n")
    f.write(f"Duplicates removed: {sales_duplicates}\n")
    f.write(f"Missing values handled: {sales_missing}\n")
    f.write(f"Records loaded successfully: {sales_loaded}\n")

print("Data quality report generated.")

import mysql.connector

MYSQL_PASSWORD = "Jikook@99"  # ONE password. Period.


# ---------------- CREATE DATABASE ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jikook@99"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS fleximart")
cursor.execute("USE fleximart")

print("Database ready")



cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date DATE
)
""")

print("customers table created")


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0
)
""")

print("products table created")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

print("orders table created")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

print("order_items table created")
conn.commit()
cursor.close()
conn.close()


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jikook@99",
    database="fleximart"
)
cursor = conn.cursor()

customer_id_map = {}

for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["first_name"],
        row["last_name"],
        row["email"],
        row["phone"],
        row["city"],
        row["registration_date"]
    ))

    mysql_id = cursor.lastrowid
    customer_id_map[row["customer_id"]] = mysql_id

conn.commit()
print("Customers inserted with ID mapping")


product_id_map = {}

for _, row in products.iterrows():
    cursor.execute("""
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (%s, %s, %s, %s)
    """, (
        row["product_name"],
        row["category"],
        row["price"],
        row["stock_quantity"]
    ))

    mysql_id = cursor.lastrowid
    product_id_map[row["product_id"]] = mysql_id

conn.commit()
print("Products inserted with ID mapping")

for _, row in sales.iterrows():

    mysql_customer_id = customer_id_map.get(row["customer_id"])
    if mysql_customer_id is None:
        continue

    mysql_product_id = product_id_map[row["product_id"]]

    total_amount = row["quantity"] * row["unit_price"]

    # Insert order
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (%s, %s, %s)
    """, (
        mysql_customer_id,
        row["transaction_date"],
        total_amount
    ))

    order_id = cursor.lastrowid

    # Insert order item
    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        order_id,
        mysql_product_id,
        row["quantity"],
        row["unit_price"],
        total_amount
    ))

conn.commit()
print("Orders inserted with correct foreign keys")
