from sqlalchemy import create_engine
import pandas as pd
engine=create_engine("mysql+pymysql://root:2004@localhost/ecommerce")
def get_products():
    query="SELECT * FROM products"
    return pd.read_sql(query,engine)
def get_customers():
    query="SELECT * from customers"
    return pd.read_sql(query,engine)
def get_orders():
    query="SELECT * from orders"
    return pd.read_sql(query,engine)
def get_order_items():
    query="SELECT * from order_items"
    return pd.read_sql(query,engine)
