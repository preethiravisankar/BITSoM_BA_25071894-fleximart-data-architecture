# =================================================
# Importing libraries
# =================================================
import pandas as pd
from pathlib import Path
import re
from sqlalchemy import create_engine, text
import datetime

# =================================================
# DATABASE CONFIG
# =================================================

DB_URI = "mysql+pymysql://root:root@localhost/fleximart"
engine = create_engine(DB_URI)

# =================================================
# CREATE TABLES IN MYSQL DB WITH THE SCHEMA GIVEN
# =================================================
create_tables_sql = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

# Execute SQL
with engine.begin() as conn:
    for stmt in create_tables_sql.split(";"):
        if stmt.strip():
            conn.execute(text(stmt))

print("Tables created successfully")

# =================================================
# EXTRACT DATA
# =================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

customers_df = pd.read_csv(DATA_DIR / "customers_raw.csv")
products_df = pd.read_csv(DATA_DIR / "products_raw.csv")
sales_df = pd.read_csv(DATA_DIR / "sales_raw.csv")

# Normalize column names
customers_df.columns = customers_df.columns.str.strip().str.lower()
products_df.columns = products_df.columns.str.strip().str.lower()
sales_df.columns = sales_df.columns.str.strip().str.lower()

# =================================================
# REMOVE DUPLICATES
# =================================================
# Before removing duplicates
rows_before_customers = customers_df.shape[0]
rows_before_sales = sales_df.shape[0]

# 1. Remove exact duplicate rows (all columns must match)
customers_df = customers_df.drop_duplicates()
sales_df = sales_df.drop_duplicates()

# After removing duplicates
rows_after_customers = customers_df.shape[0]
rows_after_sales = sales_df.shape[0]
# Calculate how many rows were removed
duplicates_removed_customers = rows_before_customers - rows_after_customers
duplicates_removed_sales = rows_before_sales - rows_after_sales

# 2. Reset the index so it's continuous again
customers_df = customers_df.reset_index(drop=True)
sales_df = sales_df.reset_index(drop=True)

# Current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_path = BASE_DIR / "data_quality_report.txt"
# Write to text file (append mode)
with open(report_path, "w") as file:
    file.write(f"[{timestamp}]\n")
    file.write(f"Duplicate removal for Customers data\n")
    file.write(f"Rows before: {rows_before_customers}\n")
    file.write(f"Rows after: {rows_after_customers}\n")
    file.write(f"Duplicates removed: {duplicates_removed_customers}\n")
    file.write("-" * 40 + "\n")

    file.write(f"[{timestamp}] Duplicate removal for Sales data\n")
    file.write(f"Rows before: {rows_before_sales}\n")
    file.write(f"Rows after: {rows_after_sales}\n")
    file.write(f"Duplicates removed: {duplicates_removed_sales}\n")
    file.write("-" * 40 + "\n")

# ===================================================================
# Handling rows with missing product_id & customer_id in sales data
# ===================================================================

#Handling missing customer_id
missing_customer = sales_df["customer_id"].isna().sum()

rows_before = sales_df.shape[0]
#drop rows with missing values
sales_df = sales_df.dropna(subset=["customer_id"])

rows_after = sales_df.shape[0]
rows_dropped = rows_before - rows_after

#Note it in data_quality_report
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Dropped invalid sales records\n")
    file.write("Reason: A sales record without connection to customers is not usedful in analysis. Also the rows with missing customer_d has status as Pending. So these rows does not contribute to revenue as well. \n")
    file.write(f"Missing customer_id rows: {missing_customer}\n")
    file.write(f"Total rows dropped based on missing customer_ids: {rows_dropped}\n")
    file.write("-" * 40 + "\n")

#Handling missing product_id
# create a price → product_id mapping from products_df
price_to_product = (
    products_df
    .drop_duplicates(subset=["price"])
    .set_index("price")["product_id"]
)
missing_product = sales_df["product_id"].isna().sum()
# fill missing product_id in sales_df using unit_price
sales_df.loc[sales_df["product_id"].isna(), "product_id"] = (
    sales_df.loc[sales_df["product_id"].isna(), "unit_price"]
    .map(price_to_product)
)

missing_product_after = sales_df["product_id"].isna().sum()
#Note it in data_quality_report
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Handlng missing product_ids in sales data\n")
    file.write("Based on the product price,  the product_id is taken from products data. (this was unique in this case)\n")
    file.write(f"Missing product_id rows: {missing_product}\n")
    file.write(f"Missing product_ids after replacement: {missing_product_after}\n")
    file.write("-" * 40 + "\n")

# ===================================================================
# Handle missing values in customer table
# ===================================================================
#Handle missing values in customer table
before = customers_df.shape[0]
missing_email_count = customers_df["email"].isna().sum()
customers_df["email_missing_flag"] = customers_df["email"].isna().astype(int)
customers_df["email"] = customers_df["email"].fillna(
    "unknown_" + customers_df["customer_id"].astype(str) + "@dummy.com"
)
#customers_df["email"] = customers_df["email"].fillna("unknown")
after = customers_df.shape[0]

#note changes in data_quality_report text file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Missing email handling (customers_csv)\n")
    file.write("Column: email\n")
    file.write(f"Missing values found: {missing_email_count}\n")
    file.write("Action taken: Filled with 'unknown_customerid@dummy.com'\n")
    #file.write("Rows affected: 5\n")
    file.write("-" * 40 + "\n")

# Calculate total sales value
sales_df["total_sales_value"] = sales_df["unit_price"] * sales_df["quantity"]

# Flag rows where product_id is missing
#sales_df["product_linked_flag"] = sales_df["product_id"].notna().astype(int)

# Separate product-unassigned sales (optional, for reporting/audit)
#sales_unassigned_product_df = sales_df[sales_df["product_id"].isna()]

# Keep product-linked sales for product-level analytics
#sales_product_level_df = sales_df[sales_df["product_id"].notna()]

# ===================================================================
# Standardize category column in products table
# ===================================================================

#change all values in cateogory column to sentence case.
products_df["category"] = products_df["category"].str.strip().str.lower().str.capitalize()

# ===================================================================
# Standardize category column in products table
# ===================================================================

#Calculate the price of missing value based on the median value of prices of same categories.
missing_before = products_df["price"].isna().sum()
category_price_median = (
    products_df
    .groupby("category")["price"]
    .median()
)
products_df["price"] = products_df["price"].fillna(
    products_df["category"].map(category_price_median)
)

#Note it in the data_quality_report 
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Missing price handling (products_csv)\n")
    file.write("Column: price\n")
    file.write("Strategy: Category-wise median calculation\n")
    file.write(f"Missing values handled: {missing_before}\n")
    file.write("-" * 40 + "\n")

#Handling missing stock price value
stock_missing_before = products_df["stock_quantity"].isna().sum()
#Filling missing stock value with zero
products_df["stock_quantity"] = products_df["stock_quantity"].fillna(0)
stock_missing_after = products_df["stock_quantity"].isna().sum()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Missing stock value handling (products_csv)\n")

    file.write("Column: stock_quantity\n")
    file.write(f"Missing before: {stock_missing_before}\n")
    file.write("Action: Filled with 0 (assumed out of stock)\n\n")
    file.write("-" * 40 + "\n")
# ===================================================================
# Standardize phone number
# ===================================================================
#Function to standardize phone in customers data
def standardize_phone(phone):
    if pd.isna(phone):
        return None

    # Remove all non-digit characters
    digits = re.sub(r"\D", "", str(phone))

    # Indian mobile numbers → last 10 digits
    if len(digits) >= 10:
        return "+91-" + digits[-10:]
    
    # Invalid phone number
    return None

customers_df["phone"] = customers_df["phone"].apply(standardize_phone)
# ===================================================================
# Standardize transaction_date in sales dataframe
# ===================================================================
# Store the total number of records before starting
total_records = len(sales_df)

# 1. Convert the column to datetime objects
# 'format='mixed' tells pandas to infer the format for each element independently
sales_df['transaction_date'] = pd.to_datetime(sales_df['transaction_date'], format='mixed')

# 2. If you need the column to stay as a string in 'YYYY-MM-DD' format:
sales_df['transaction_date'] = sales_df['transaction_date'].dt.strftime('%Y-%m-%d')
#print(sales_df)

# 3. Store the counts in variables
# .count() only counts non-null/non-NaT values
successful_count = sales_df['transaction_date'].count()
failed_count = sales_df['transaction_date'].isna().sum()

#Note it in the data_quality_report 
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Standardizing dates in sales data\n")
    file.write("Column: transaction_date\n")
    file.write("Strategy: convert to YYY-MM-DD format\n")
    file.write(f"Successfully handled records: {successful_count}\n")
    file.write(f"Invalid dates (failed): {failed_count}\n")
    file.write("-" * 40 + "\n")

# ===================================================================
# Standardize registration_date in customers table
# ===================================================================
# Store the total number of records before starting
total_records = len(sales_df)

# 1. Convert the column to datetime objects
# 'format='mixed' tells pandas to infer the format for each element independently
customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'], format='mixed')

# 2. If you need the column to stay as a string in 'YYYY-MM-DD' format:
customers_df['registration_date'] = customers_df['registration_date'].dt.strftime('%Y-%m-%d')
#print(sales_df)

# 3. Store the counts in variables
# .count() only counts non-null/non-NaT values
successful_count = customers_df['registration_date'].count()
failed_count = customers_df['registration_date'].isna().sum()

#Note it in the data_quality_report 
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(report_path, "a") as file:
    file.write(f"[{timestamp}] Standardizing dates in customer data\n")
    file.write("Column: registration_date\n")
    file.write("Strategy: convert to YYY-MM-DD format\n")
    file.write(f"Successfully handled records: {successful_count}\n")
    file.write(f"Invalid dates (failed): {failed_count}\n")
    file.write("-" * 40 + "\n")

# ===================================================================
# Start inserting value to tables in fleximart database
# ===================================================================
# Customer table
# ===================================================================

import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
customer_map = {} 
rows_inserted=0
try:
    with engine.begin() as conn:   # single transaction, single connection
        for _, row in customers_df.iterrows():

            result = conn.execute(
                text("""
                    INSERT INTO customers
                    (first_name, last_name, email, phone, city, registration_date)
                    VALUES (:first_name, :last_name, :email, :phone, :city, :reg_date)
                """),
                {
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "phone": row["phone"],
                    "city": row["city"],
                    "reg_date": row["registration_date"]
                }
            )
            rows_inserted+=1
            #  Auto-generated DB ID (LAST_INSERT_ID equivalent)
            db_customer_id = result.lastrowid

            #  Capture mapping
            customer_map[row["customer_id"]] = db_customer_id

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Customers table load\n")
        file.write("Table: customers\n")
        file.write(f"Rows inserted: {rows_inserted}\n")
        file.write("Action taken: Appended records from customers_df\n")
        file.write("-" * 40 + "\n")

except IntegrityError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Customers table load FAILED\n")
        file.write("Error type: IntegrityError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Duplicate or constraint violation\n")
        file.write("-" * 40 + "\n")

except SQLAlchemyError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Customers table load FAILED\n")
        file.write("Error type: SQLAlchemyError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Database or connection issue\n")
        file.write("-" * 40 + "\n")

except Exception as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Customers table load FAILED\n")
        file.write("Error type: UnexpectedError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("-" * 40 + "\n")
    
# ===================================================================
# Products table
# ===================================================================
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
rows_inserted = 0
product_map = {}

try:
    with engine.begin() as connection:
        for _, row in products_df.iterrows():

            result = connection.execute(
                text("""
                    INSERT INTO products
                    (product_name, category, price, stock_quantity)
                    VALUES (:product_name, :category, :price, :stock_quantity)
                """),
                {
                    "product_name": row["product_name"],
                    "category": row["category"],
                    "price": row["price"],
                    "stock_quantity": row["stock_quantity"]
                }
            )
            rows_inserted+=1
            # auto-incremented DB product_id
            db_product_id = result.lastrowid

            # map CSV product_id (P001) → DB product_id (1,2,3…)
            product_map[row["product_id"]] = db_product_id

    # SUCCESS log
    
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Products table load\n")
        file.write("Table: products\n")
        file.write(f"Rows inserted: {rows_inserted}\n")
        file.write("Action taken: Appended records from products_df\n")
        file.write("-" * 40 + "\n")

except IntegrityError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Products table load FAILED\n")
        file.write("Error type: IntegrityError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Duplicate or constraint violation\n")
        file.write("-" * 40 + "\n")

except SQLAlchemyError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Products table load FAILED\n")
        file.write("Error type: SQLAlchemyError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Database or connection issue\n")
        file.write("-" * 40 + "\n")

except Exception as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Products table load FAILED\n")
        file.write("Error type: UnexpectedError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("-" * 40 + "\n")
# ===================================================================
# Orders table
# ===================================================================
#Convert customer_map to a DataFrame and merge with sales data
# This is to use the mapped dataframe where customer_id in dataset is mapped with customer_id auto-increment column in database
customer_map_df = pd.DataFrame(
    customer_map.items(),
    columns=["customer_id", "db_customer_id"]
)
sales_with_customer_df = sales_df.merge(
    customer_map_df,
    on="customer_id",
    how="left"
)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
rows_inserted = 0
order_map = {}  
try:
   with engine.begin() as connection:
    for _, row in sales_with_customer_df.iterrows():

        total_amount = row["quantity"] * row["unit_price"]

        result = connection.execute(
            text("""
                INSERT INTO orders
                (customer_id, order_date, total_amount, status)
                VALUES (:customer_id, :order_date, :total_amount, :status)
            """),
            {
                "customer_id": row["db_customer_id"],
                "order_date": row["transaction_date"],
                "total_amount": total_amount,
                "status": row["status"]
            }
        )
        rows_inserted+=1
        # auto-generated order_id
        db_order_id = result.lastrowid

        # map CSV transaction_id → DB order_id
        order_map[row["transaction_id"]] = db_order_id

    # SUCCESS log
   
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load\n")
        file.write("Table: orders\n")
        file.write(f"Rows inserted: {rows_inserted}\n")
        file.write("Action taken: Appended records from sales dataset\n")
        file.write("-" * 40 + "\n")

except IntegrityError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: IntegrityError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Foreign key or constraint violation\n")
        file.write("-" * 40 + "\n")

except SQLAlchemyError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: SQLAlchemyError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Database or connection issue\n")
        file.write("-" * 40 + "\n")

except Exception as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: UnexpectedError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("-" * 40 + "\n")
# ===================================================================
# Order Items table
# ===================================================================
#Convert order_map to a DataFrame and merge with sales data

order_map_df = pd.DataFrame(
    order_map.items(),
    columns=["transaction_id", "db_order_id"]
)
#Convert product_map to a DataFrame and merge with sales data
product_map_df = pd.DataFrame(
    product_map.items(),
    columns=["product_id", "db_product_id"]
)
# This is to use the mapped dataframe where transaction_id in dataset is mapped with order_id auto-increment column in database(order table)
sales_with_order_df = sales_df.merge(
    order_map_df,
    on="transaction_id",
    how="left"
)
# This is to use the mapped dataframe where product_id in dataset is mapped with product_id auto-increment column in database (product table)
sales_with_product_df = sales_with_order_df.merge(
    product_map_df,
    on="product_id",
    how="left"
)
order_item_map={}
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
rows_inserted = 0
try:
   with engine.begin() as connection:
    for _, row in sales_with_product_df.iterrows():

        result = connection.execute(
            text("""
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
            """),
            {
                "order_id": row["db_order_id"],
                "product_id": row["db_product_id"],
                "quantity": row["quantity"],
                "unit_price": row["unit_price"],
                "subtotal": row["total_sales_value"]
            }
        )
        rows_inserted+=1
        # auto-generated order_id
        db_order_item_id = result.lastrowid

        # map CSV transaction_id → DB order_item_id
        order_item_map[row["transaction_id"]] = db_order_item_id

    # SUCCESS log
   
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Order Items table load\n")
        file.write("Table: order_items\n")
        file.write(f"Rows inserted: {rows_inserted}\n")
        file.write("Action taken: Appended records from sales dataset\n")
        file.write("-" * 40 + "\n")

except IntegrityError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: IntegrityError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Foreign key or constraint violation\n")
        file.write("-" * 40 + "\n")

except SQLAlchemyError as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: SQLAlchemyError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("Likely cause: Database or connection issue\n")
        file.write("-" * 40 + "\n")

except Exception as e:
    with open(report_path, "a") as file:
        file.write(f"[{timestamp}] Orders table load FAILED\n")
        file.write("Error type: UnexpectedError\n")
        file.write(f"Error message: {str(e)}\n")
        file.write("-" * 40 + "\n")
