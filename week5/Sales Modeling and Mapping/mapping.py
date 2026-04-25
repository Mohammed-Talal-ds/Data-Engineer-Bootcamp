import pandas as pd
from sqlalchemy import create_engine

source_engine = create_engine(
    "postgresql+psycopg2://postgres:admin@localhost:5432/commerce"
)

target_engine = create_engine(
    "postgresql+psycopg2://postgres:admin@localhost:5432/ecommerce_dw"
)

orders = pd.read_sql("SELECT * FROM orders", source_engine)
order_items = pd.read_sql("SELECT * FROM order_items", source_engine)
products = pd.read_sql("SELECT * FROM products", source_engine)
brands = pd.read_sql("SELECT * FROM brands", source_engine)
categories = pd.read_sql("SELECT * FROM categories", source_engine)
users = pd.read_sql("SELECT * FROM users", source_engine)
branches = pd.read_sql("SELECT * FROM branches", source_engine)
payments = pd.read_sql("SELECT * FROM payments", source_engine)
payment_methods = pd.read_sql("SELECT * FROM payment_methods", source_engine)
currencies = pd.read_sql("SELECT * FROM currencies", source_engine)

print("Data Extracted")


dim_products = products.merge(brands, on="brand_id", how="left") \
                       .merge(categories, on="category_id", how="left")

dim_products = dim_products[[
    "product_id", "product_name", "brand_name", "category_name"
]].drop_duplicates()

dim_users = users[[
    "user_id", "full_name", "email", "phone", "address"
]].drop_duplicates()

dim_branches = branches[[
    "branch_id", "branch_name", "city", "manager_name"
]].drop_duplicates()

dim_payment_methods = payment_methods[[
    "method_id", "method_name"
]].drop_duplicates()

dim_currencies = currencies[[
    "currency_id", "currency_code", "currency_name"
]].drop_duplicates()

orders["order_date"] = pd.to_datetime(orders["order_date"])

orders["date_id"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)

dim_date = pd.DataFrame()
dim_date["full_date"] = orders["order_date"].drop_duplicates()
dim_date["day"] = dim_date["full_date"].dt.day
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["weekday"] = dim_date["full_date"].dt.day_name()

dim_date["date_id"] = range(1, len(dim_date) + 1)

print("Dimensions Built")



fact = order_items.merge(
    orders[[
        "order_id",
        "user_id",
        "date_id",
        "branch_id",
        "currency_id",
        "subtotal",
        "tax_amount",
        "total_amount"
    ]],
    on="order_id",
    how="left"
).merge(
    payments,
    on="order_id",
    how="left"
)




fact["profit"] = (
    fact["unit_sale_price"] - fact["unit_purchase_price"]
) * fact["quantity"]

fact_sales = fact[[
    "date_id",
    "user_id",
    "product_id",
    "branch_id",
    "currency_id",
    "method_id",
    "quantity",
    "unit_sale_price",
    "unit_purchase_price",
    "subtotal",
    "tax_amount",
    "total_amount",
    "profit"
]]

print("Fact Table Built")


print(f"Order Items Rows: {len(order_items)}")
print(f"Fact Rows: {len(fact_sales)}")

if len(order_items) != len(fact_sales):
    raise Exception("Data loss detected!")
else:
    print("No Data Loss")


dim_products.to_sql("dim_products", target_engine, if_exists="replace", index=False)
dim_users.to_sql("dim_users", target_engine, if_exists="replace", index=False)
dim_branches.to_sql("dim_branches", target_engine, if_exists="replace", index=False)
dim_payment_methods.to_sql("dim_payment_methods", target_engine, if_exists="replace", index=False)
dim_currencies.to_sql("dim_currencies", target_engine, if_exists="replace", index=False)
dim_date.to_sql("dim_date", target_engine, if_exists="replace", index=False)

fact_sales.to_sql("fact_sales", target_engine, if_exists="replace", index=False)

print("Data Loaded Successfully into ecommerce_dw")