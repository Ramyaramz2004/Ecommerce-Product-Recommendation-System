from db import get_customers
from db import get_orders
from db import get_order_items
from db import get_products
import pandas as pd
customers=get_customers()
orders=get_orders()
order_items=get_order_items()
products=get_products()
print("Customers")
print(customers)

print("\n Orders")
print(orders)

print("\n Order Items")
print(order_items)

print("\n Products")
print(products)

customer_order =pd.merge(customers,orders,on="customer_id")
print(customer_order)

customer_order_items=pd.merge(customer_order,order_items,on="order_id")
print("\n Customer Order Items")
print(customer_order_items)

final_df=pd.merge(customer_order_items,products,on="product_id")
print("\nFinal Dataset")
print(final_df)