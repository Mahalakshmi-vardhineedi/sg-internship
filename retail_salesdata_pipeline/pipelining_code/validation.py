import pandas as pd
from sqlalchemy import create_engine, text
customers = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/customers.csv")
products = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/products.csv")
sales = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/sales.csv")
stores = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/store.csv")
refunds = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/refunds.csv")

#ghadhmgdfzhtdmv tdgmbfhtgcbmvjyfdhmcvgmbf nhcftgn
# print(customers.head(),"\n")
# print(products.head(),"\n")
# print(sales.head(),"\n")
# print(stores.head(),"\n")
# print(refunds.head(),"\n")

# valid sales 
# Define mapping of words to numbers
word_to_num = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
}

# Clean and transform the 'quantity' column
sales['quantity'] = (
    sales['quantity']
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace('\xa0', ' ', regex=False)  # replace non-breaking spaces
    .replace(word_to_num)                   # replace words with numbers
)

#Convert to numeric, coerce errors to NaN
sales['quantity'] = pd.to_numeric(sales['quantity'], errors='coerce')
valid_sales = sales[sales['quantity'] > 0 & sales['product_id'].notnull()]
invalid_sales = sales[~sales.index.isin(valid_sales.index)]
sales = valid_sales
# print(len(valid_sales),valid_sales)
# print(len(invalid_sales),invalid_sales)

# valid products
categories = ["Electronics", "Furniture", "Clothing", "Beauty", "Sports"]
valid_products = products[products['category'].isin(categories) & products['product_id'].notnull()]
invalid_products = products[~products.index.isin(valid_products.index)]
products = valid_products
# print(len(valid_products), valid_products)
# print(len(invalid_products), invalid_products)
# print(len(products),products)

#valid customers
invalid_customers = customers[customers['customer_id'].isnull() | customers['name'].isnull() | customers['location'].isnull()]
valid_customers = customers[~customers.index.isin(invalid_customers.index)]
customers = valid_customers
# print(len(invalid_customer), invalid_customer)
# print(len(valid_customers), valid_customers)

#valid stores
invalid_stores = stores[stores['store_id'].isnull() | stores['store_name'].isnull()| stores['city'].isnull()]
valid_stores = stores[~stores.index.isin(invalid_stores.index)]
stores = valid_stores
# print(valid_stores, len(valid_stores))
# print(invalid_stores, len(invalid_stores))

#valid refunds
invalid_refunds = refunds[refunds['reason'].isnull() | refunds['id'].isnull()]
valid_refunds = refunds[~refunds.index.isin(invalid_refunds.index)]
refunds = valid_refunds
# print(invalild_refunds,len(invalild_refunds))
# print(valild_refunds,len(valild_refunds))

print("Number of metrics rejected in sales:", len(invalid_sales))
print("Number of metrics processed in sales:", len(valid_sales))
print("Number of metrics rejected in products:", len(invalid_products))
print("Number of metrics processed in products:", len(valid_products))
print("Number of metrics rejected in customers:", len(invalid_customers))
print("Number of metrics processed in customers:", len(valid_customers))
print("Number of metrics rejected in stores:", len(invalid_stores))
print("Number of metrics processed in stores:", len(valid_stores))
print("Number of metrics rejected in refunds:", len(invalid_refunds))
print("Number of metrics processed in refunds:", len(valid_refunds))

# 3. LOAD into MySQL
# MySQL connection parameters
mysql_user = "root"
mysql_password = "08052004"
mysql_host = "localhost"     # or IP if remote
mysql_port = "3306"
mysql_database = "Retail_db"

# SQLAlchemy connection string
connection_str = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
engine = create_engine(connection_str)

# Load the dataframe to a MySQL table
products.to_sql("products", con=engine, if_exists="replace", index=False)
sales.to_sql("sales", con=engine, if_exists="replace", index=False)
refunds.to_sql("refunds", con=engine, if_exists="replace", index=False)
stores.to_sql("stores", con=engine, if_exists="replace", index=False)
customers.to_sql("customers", con=engine, if_exists="replace", index=False)
# sales.product_id,sales.quantity * sales.unit_price as revenue
top5_reasons = """
SELECT reason
FROM refunds
GROUP BY reason
ORDER BY COUNT(*) DESC LIMIT 5;
"""
df_top5_reasons = pd.read_sql(top5_reasons, con=engine)
print(df_top5_reasons)

df_top5_products = """
SELECT s.product_id,ROUND(SUM((s.unit_price * s.quantity) - r.refund_amount),2) AS revenue 
FROM sales s JOIN refunds r ON s.product_id = r.product_id
GROUP BY s.product_id 
ORDER BY revenue DESC
LIMIT 5;
"""
df_top5_products = pd.read_sql(df_top5_products, con=engine)
print(df_top5_products)

df_top5_customers = """
SELECT c.customer_id, c.name, ROUND(SUM(s.quantity * s.unit_price - r.refund_amount),2) AS revenue
FROM sales s JOIN refunds r ON s.sale_id = r.order_id JOIN customers c ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.name
ORDER BY revenue DESC LIMIT 5;
"""
df_top5_customers = pd.read_sql(df_top5_customers, con=engine)
print(df_top5_customers)