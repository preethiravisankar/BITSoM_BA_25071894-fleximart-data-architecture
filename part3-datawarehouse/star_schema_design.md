# Part 3-Task 3.1: Star Schema Design Documentation

## 1. Section 1: Schema Overview

### Describing the star schema

**FACT TABLE: fact_sales**  
Grain: One row per product per order line item  
Business Process: Sales transactions

Measures (Numeric Facts):
- quantity_sold: Number of units sold
- unit_price: Price per unit at time of sale
- discount_amount: Discount applied
- total_amount: Final amount (quantity × unit_price - discount)

Foreign Keys:
- date_key → dim_date
- product_key → dim_product
- customer_key → dim_customer

**DIMENSION TABLE: dim_date**  
Purpose: Date dimension for time-based analysis  
Type: Conformed dimension
Attributes:
- date_key (PK): Surrogate key (integer, format: YYYYMMDD)
- full_date: Actual date
- day_of_week: Monday, Tuesday, etc.
- month: 1-12
- month_name: January, February, etc.
- quarter: Q1, Q2, Q3, Q4
- year: 2023, 2024, etc.
- is_weekend: Boolean

**DIMENSION TABLE: dim_product**  
Purpose: Product description for product-based analysis  
Type: Descriptive dimension
Attributes:
- product_key (PK): Surrogate key (Integer-autoincrement) 
- product_id: Product identifier from the source data
- product name: Name of product
- category: Category of product (electronics, groceries, fresh, fashion etc)
- subcategory: Specific classification of category (for electronics category, it can be laptop, phone, headset etc)
- unit_price: Price of a single unit of product

**DIMENSION TABLE: dim_customer**  
Purpose: Customer details for customer-based analysis  
Type: Descriptive dimension
Attributes:
- customer_key (PK): Surrogate key (Integer-autoincrement)
- customer_id: Customer identifier from the source data
- customer_name: Customer name
- city: Customer residence city
- state: State in which customer resides
- customer-segment: Grouping based on behavior (regular/premium/new/wholesale)

## 2. Section 2: Design Decisions

- The fact table uses transaction line-item granularity, meaning one row per product per order. This level was chosen because it captures the most detailed sales information, such as product-level quantity, price, and discounts. It allows Fleximart to perform detailed analysis while still supporting aggregated reporting.
- Surrogate keys are used instead of natural keys because they are stable, system-generated, and efficient. Natural keys such as product IDs or customer emails can change over time and may affect data consistency. Surrogate keys, which are normally integers, also improve query performance and help manage historical changes in dimension data.
- This star schema design supports roll-up and drill-down operations by separating measures and descriptive attributes. Users can roll up data to higher levels (monthly or yearly sales) or drill down to detailed levels (daily sales or individual products or gender/age preference) using the dimension attributes.

## Section 3: Sample Data Flow

Source Transaction:  
Order #102, Customer "Preethi Ravi", Product "Cotton T Shirt", Qty: 2, Unit_price: 300

Becomes in Data Warehouse:  
fact_sales:  
 {  
  sale_key: (auto-increment integer)  
  date_key: 20261226,  
  product_key: 10,  
  customer_key: 16,  
  quantity_sold: 3,  
  unit_price: 300,  
  discount_amount: 30  
  total_amount: 870  
}

dim_date: {date_key: 20261226, full_date: '2026-12-26', day_of_week: 4, day_of_month:26, month:12, month_name: 'December', quarter: 'Q3', year: 2026, is_weekend: false }  
dim_product: {product_key: 10, product_name: 'Cotton T Shirt', category: 'Fashion', sub-category: 'Women-Tops', unit_price: 300}  
dim_customer: {customer_key: 16, customer_name: 'Preethi Ravi'', city: 'Chennai', state: 'Tamilnadu', customer_segment: 'premium'}
