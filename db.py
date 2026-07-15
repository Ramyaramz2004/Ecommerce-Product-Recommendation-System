from sqlalchemy import create_engine
import pandas as pd
import os

HOST = os.getenv("MYSQLHOST")
PORT = os.getenv("MYSQLPORT")
DATABASE = os.getenv("MYSQLDATABASE")
USER = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQLPASSWORD")

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

def get_products():
    return pd.read_sql("SELECT * FROM products", engine)

def get_customers():
    return pd.read_sql("SELECT * FROM customers", engine)

def get_orders():
    return pd.read_sql("SELECT * FROM orders", engine)

def get_order_items():
    return pd.read_sql("SELECT * FROM order_items", engine)