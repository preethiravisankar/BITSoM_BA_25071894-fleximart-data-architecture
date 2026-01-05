# Database Schema Documentation

## 1. Entity–Relationship Description

### ENTITY: customers
Purpose: Stores customer information.

Attributes:
- customer_id: Unique identifier (Auto increment Primary Key)
- first_name: Customer’s first name
- last_name: Customer’s last name
- email: Customer’s email address (unique)
- phone: Customer’s phone number 
- city: Customer’s city
- registration_date: Date the customer registered

Relationships:
- One customer can place many orders (1 to many with orders table)

### ENTITY: products
Purpose: Stores product information.

Attributes:
- product_id: Unique identifier (Auto increment Primary Key)
- product_name: Name of the product
- category: The category of the product (like electronics, fashion, groceries etc )
- price: Cost of the product
- stock_quantity: Number of products in stock (default is zero) 

Relationships:
- One product can appear in many places in order_items (1 to many with order_items table)

### ENTITY: orders
Purpose: Records order level details for purchases made by customer.

Attributes:
- order_id: Unique identifier (Auto increment Primary Key)
- customer_id: Identifier of the customer who placed the order (Foreign Key referencing customers.customer_id)
- order_date: The date the order was placed/transaction happened.
- total_amount: Derived column - product of quantity and price of each transaction in salesraw_csv.
- status: The completion status of the transaction (pending/completed/cancelled)

Relationships:
- One customer can appear in many rows in order_items (many to one with customers table)
- One order appears once in the order_items table (one to one with order_items table)

### ENTITY: order_items
Purpose: Records transaction/order details for each product included in an order.

Attributes:
- order_item_id: Unique identifier (Auto increment Primary Key)
- order_id: Identifier of the order to which the item belongs (Foreign Key referencing orders.order_id)
- product_id: Identifier of the product ordered (Foreign Key referencing products.product_id)
- quantity: Number of units of the product ordered
- unit_price: Price per unit of the product at the time of order
- subtotal: Derived column - product of quantity and price of each transaction in salesraw_csv.

Relationships:
- One product can appear in many rows in order_items (many to one with products table)
- One order appears once in the order table (one to one with order table)

## 2. Normalisation Explanation

The given database design is in Third Normal Form (3NF) because it satisfies all the requirements of First, Second, and Third Normal Forms.

**First Normal Form (1NF):** These conditions of 1NF are satisfied:
- *No repetition*: Details like customer information, product information are not repeated and stored in separate tables. 
- *Atomicity*: Each cell contains only one piece of information. (no comma-separated values)
- *Unique* rows with primary key: Each row in all the tables can be identified by primary key of that table.

**Second Normal Form(2NF):** To satisfy 2NF, we must remove ***partial dependencies***, where all non-key attributes are fully functionally dependent on the entire primary key of their respective tables.
For example, in orders table, the order_date, total_amount, status are entirely dependent on the order_id. In the order_items table, attributes like quantity, unit_price, and subtotal depend on the primary key (order_item_id).

**Third Normal Form(3NF):** To satisfy 3rd Normal form condition, we must remove ***transitive dependencies***, which means the non-key attributes should not depend on other non-key attributes. In the given schema, this condition is satisfied because customer attributes such as first_name, last_name, and email depend only on customer_id and are stored in the customers table, not in the orders table. Similarly, product attributes like product_name, category, and price depend only on product_id and are stored exclusively in the products table. Hence, there are no transitive dependencies, and the schema is in 3NF.

### Functional dependencies
*(X → Y means X functionally determines Y)*
* customer_id → first_name, last_name, email, phone, city, registration_date
* product_id → product_name, category, price, stock_quantity
* order_id → customer_id, order_date, total_amount, status
* order_item_id → order_id, product_id, quantity, unit_price, subtotal

### How this design avoids the three anamolies

| Anamoly   | How we have avoided it |
| --------  | ------- |
| Insert    | You can add a new Product or customer to the database even if the product has not been bought or the customer has not purchased.    |
| Update    | If a customer changes their Email, you only update one row in the Customers table. If the prouct stock_quantity or price changes, it will be udpated in the products table. The price update will not affect the previously entered rows.      |
| Delete    | If you delete a specific Order, you don't lose the Customer's contact info or the Product's description. The entities exist independently of the transaction.    |

## 3. Sample Data Representation

### Customers table:

| customer_id | first_name | last_name | email                     | phone         | city      | registration_date |
|------------|------------|-----------|---------------------------|---------------|-----------|-------------------|
| 1          | Rahul      | Sharma    | rahul.sharma@gmail.com    | +91-9876543210| Bangalore | 2023-01-15        |
| 2          | Priya      | Patel     | priya.patel@yahoo.com     | +91-9988776655| Mumbai    | 2023-02-20        |
| 3          | Amit       | Kumar     | unknown_C003@dummy.com    | +91-9765432109| Delhi     | 2023-03-10        |

### Products table:

| product_id | product_name         | category    | price   | stock_quantity |
|-----------|----------------------|-------------|---------|----------------|
| 1         | Samsung Galaxy S21   | Electronics | 45999.00| 150            |
| 2         | Nike Running Shoes   | Fashion     | 3499.00 | 80             |
| 3         | Apple MacBook Pro    | Electronics | 32999.00| 45             |

### Orders table:

| order_id | customer_id | order_date | total_amount | status    |
|---------|-------------|------------|--------------|-----------|
| 1       | 1           | 2024-01-15 | 45999.00     | Completed |
| 2       | 2           | 2024-01-16 | 5998.00      | Completed |
| 3       | 3           | 2024-01-15 | 52999.00     | Completed |

### Order Items table:

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------|----------|------------|----------|------------|----------|
| 1            | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2            | 2        | 4          | 2        | 2999.00    | 5998.00  |
| 3            | 3        | 7          | 1        | 52999.00   | 52999.00 |



