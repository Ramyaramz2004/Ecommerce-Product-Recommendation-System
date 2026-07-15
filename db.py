from sqlalchemy import create_engine
import pandas as pd
import os

DATABASE_URL = os.getenv("MYSQL_URL")

# Convert Railway URL to use PyMySQL
DATABASE_URL = DATABASE_URL.replace(
    "mysql://",
    "mysql+pymysql://"
)

engine = create_engine(DATABASE_URL)

def get_products():
    return pd.read_sql("SELECT * FROM products", engine)

def get_customers():
    return pd.read_sql("SELECT * FROM customers", engine)

def get_orders():
    return pd.read_sql("SELECT * FROM orders", engine)

def get_order_items():
    return pd.read_sql("SELECT * FROM order_items", engine)