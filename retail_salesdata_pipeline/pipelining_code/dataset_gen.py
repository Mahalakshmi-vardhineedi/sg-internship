# import pandas as pd
# from sqlalchemy import create_engine, text

# # Load CSV into DataFrame
# df = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/product.csv")

# # MySQL connection parameters
# mysql_user = "root"
# mysql_password = "08052004"
# mysql_host = "localhost"
# mysql_port = "3306"
# mysql_database = "PRODUCTS_DB"

# # SQLAlchemy connection string
# connection_str = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
# engine = create_engine(connection_str)

# # Load the dataframe to a MySQL table
# df.to_sql("products", con=engine, if_exists="replace", index=False)

# # Define queries
# queries = [
#     """
#     UPDATE products
#     SET category = 'Furniture'
#     WHERE category IN ('Home & Living','Kitchenware')
#     """,
#     """
#     UPDATE products
#     SET category = 'Beauty'
#     WHERE category IN ('Personal Care', 'Footwear')
#     """,
#     """
#     DELETE FROM products
#     WHERE category = 'Grocery'
#     """
# ]

# # Execute queries one by one
# with engine.connect() as conn:
#     for q in queries:
#         conn.execute(text(q))
#     conn.commit()

# # Final SELECT query
# select_query = """
# SELECT
#     ANY_VALUE(product_id) AS product_id,
#     product_name,
#     ANY_VALUE(category) AS category,
#     ANY_VALUE(price) AS price
# FROM products
# GROUP BY product_name
# """

# # Read the result into DataFrame
# df_result = pd.read_sql(select_query, con=engine)

# # Save the result to CSV
# # df_result.to_csv("product2.csv", index=False)
# df1 = pd.read_csv('product1.csv')
# df2 = pd.read_csv('product2.csv')

# # Concatenate the DataFrames
# merged_df = pd.concat([df1, df2], ignore_index=True)

# # Save the merged DataFrame to a new CSV file
# merged_df.to_csv('merged_appended.csv', index=False)
# import pandas as pd
# from sqlalchemy import create_engine, text
# # Load CSV into DataFrame
# df = pd.read_csv(r"C:\Users\mounika chintakayala\Desktop\intern\project\merged_appended.csv")
# # MySQL connection parameters
# mysql_user="root"
# mysql_host="localhost"
# mysql_password="08052004"
# mysql_port="3306"
# mysql_database="PRODUCTS_DB"
# # SQLAlchemy connection string
# connection_str = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
# engine = create_engine(connection_str)
# # Load the dataframe to a MySQL table
# df.to_sql("products", con=engine, if_exists="replace", index=False)
# query= """
# SELECT
# 	ANY_VALUE(product_id) AS product_id,
# 	product_name,
# 	ANY_VALUE(category) AS category,
# 	ANY_VALUE(price) AS price
# FROM products
# group by product_name;
# """
# # Read the result into DataFrame
# df_result = pd.read_sql(query, con=engine)
# # Save the result to CSV
# df_result.to_csv("product.csv", index=False)

# #sales data preparation
# import pandas as pd
# import random
# from faker import Faker
# import uuid

# # Load input files
# products = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/products.csv")
# stores = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/stores.csv")
# customers = pd.read_excel("C:/Users/mounika chintakayala/Desktop/intern/project/customers.xlsx")


# fake = Faker()
# num_records = 5000  # You can increase this as needed

# sales_data = []

# for i in range(num_records):
#     product = products.sample().iloc[0]
#     customer = customers.sample().iloc[0]
#     store = stores.sample().iloc[0]
    
#     sale_id = str(uuid.uuid4())
#     product_id = product['product_id']
#     customer_id = customer['customer_id']
#     store_id = store['store_id']
#     quantity = random.randint(1, 5)
#     unit_price = product['price']
#     date = fake.date_between(start_date='-30d', end_date='today')

#     sales_data.append({
#         'sale_id': sale_id,
#         'product_id': product_id,
#         'customer_id': customer_id,
#         'date': date.strftime("%Y-%m-%d"),
#         'store_id': store_id,
#         'quantity': quantity,
#         'unit_price': unit_price
#     })

# # Convert to DataFrame
# sales_df = pd.DataFrame(sales_data)
# print(sales_df['date'])

# # Save to CSV
# sales_df.to_csv("sales.csv", index=False)

# print("✅ sales.csv generated successfully with", num_records, "records.")


# #refunds data preparation
# import pandas as pd
# import uuid
# import random

# # Load sales and product data
# sales = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/sales.csv")
# products = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/products.csv")

# # Merge sales with product category info
# merged = pd.merge(sales, products[['product_id', 'category']], on='product_id', how='left')

# # Refund reasons by category
# refund_reasons = {
#     "Electronics": [
#         "Defective item", "Not as described", "Overheating issue", "Item not working",
#         "Short circuit", "Battery issue", "Screen cracked", "Connectivity problems",
#         "Doesn’t support features", "Power issue"
#     ],
#     "Furniture": [
#         "Damaged corner", "Wrong size", "Missing parts", "Color mismatch",
#         "Assembly issues", "Wobbly structure", "Wood chipped", "Scratched surface",
#         "Doesn’t fit room", "Incorrect product"
#     ],
#     "Clothing": [
#         "Wrong size", "Color mismatch", "Damaged item", "Poor quality material",
#         "Stitching coming off", "Fabric too thin", "Shrinkage after wash",
#         "Not as shown in image", "Uncomfortable fabric", "Button missing"
#     ],
#     "Beauty": [
#         "Allergic reaction", "Wrong product delivered", "Opened packaging",
#         "Irritated skin", "Wrong shade", "Product expired", "Broken bottle",
#         "Seal broken", "Strong fragrance", "No visible results"
#     ],
#     "Sports": [
#         "Not as expected", "Damaged in shipping", "Wrong item sent",
#         "Poor grip", "Low quality material", "Size mismatch",
#         "Equipment malfunction", "Item not durable", "Handle broken",
#         "Missing accessories"
#     ]
# }

# num_refunds = len(merged)
# refund_sales = merged.sample(n=num_refunds)
# refunds = []

# for _, row in refund_sales.iterrows():
#     refund_id = str(uuid.uuid4())
#     order_id = row['sale_id']
#     product_id = row['product_id']
#     category = row['category']
#     quantity = row['quantity']
#     unit_price = row['unit_price']
    
#     # Calculate max refund value
#     max_refund = quantity * unit_price
#     refund_amount = round(random.uniform(0.3 * max_refund, max_refund), 2)  # At least 30%

#     # Choose refund reason based on category
#     reasons = refund_reasons.get(category, ["General dissatisfaction", "No longer needed"])
#     reason = random.choice(reasons)

#     refunds.append({
#         "id": str(uuid.uuid4()),
#         "order_id": order_id,
#         "product_id": product_id,
#         "reason": reason,
#         "refund_amount": refund_amount
#     })

# # Convert to DataFrame and save
# refunds_df = pd.DataFrame(refunds)
# refund_sample = refunds_df.sample(n=750, random_state=42)
# refund_sample.to_csv("refunds.csv", index=False)

# print(f"✅ Generated {len(refund_sample)} refund records and saved to refunds.csv")


#checking the data

import pandas as pd
from sqlalchemy import create_engine, text
products = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/products.csv")
stores = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/stores.csv")
customers = pd.read_excel("C:/Users/mounika chintakayala/Desktop/intern/project/customers.xlsx")
sales = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/sales.csv")
refunds = pd.read_csv("C:/Users/mounika chintakayala/Desktop/intern/project/refunds.csv")
#read the data into the data base
mysql_user = "root"
mysql_password = "08052004"
mysql_host = "localhost"
mysql_port = "3306"
mysql_database = "PRODUCTS_DB"
# SQLAlchemy connection string
connection_str = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
engine = create_engine(connection_str)
# Load the dataframes to MySQL tables
products.to_sql("products", con=engine, if_exists="replace", index=False)
stores.to_sql("stores", con=engine, if_exists="replace", index=False)
customers.to_sql("customers", con=engine, if_exists="replace", index=False)
sales.to_sql("sales", con=engine, if_exists="replace", index=False)
refunds.to_sql("refunds", con=engine, if_exists="replace", index=False)
