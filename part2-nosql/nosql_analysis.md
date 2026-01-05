# Part 2: NoSQL Justification Report

## 1. Section A: Limitations of RDBMS

### Question: Explain why the current relational database would struggle with the following:
- Products having different attributes (e.g., laptops have RAM/processor, shoes have size/color)
- Frequent schema changes when adding new product types
- Storing customer reviews as nested data

### Answer:

- Relational databases like MySQL work well when data is structured and uniform, but they struggle with highly diverse product data. In Fleximart, products cannot be described using a fixed set of attributes. For example, Puma sneakers require attributes like size, gender, and color variants, while laptops need RAM, processor, and graphics card details. In an RDBMS, this leads to many nullable columns or multiple product tables, making the design complex and inefficient.
- Additionally, the rigid schema means that adding new product types requires altering table structures, which is time-consuming and risky for large datasets. This also affects existing applications that depend on the schema.
- Storing customer reviews is also challenging. In real-world, customer reviews can be in the form of text, image, video, likes etc. and hence requires multiple tables and joins to represent one-to-many relationships, which increases query complexity and reduces performance when fetching product details along with reviews.

## 2. Section B: NoSQL Benefits 

### Question: Explain how MongoDB solves these problems using the following:
- Flexible schema (document structure)
- Embedded documents (reviews within products)
- Horizontal scalability

### Answer:

- A flexible document-based schema will address the diverse variety of data. Each product or review can be stored as a JSON like doucment with only the attributes that it needs. For example,  a shoe product can store attributes like brand, gender, color; while a phone product can store like memory, color, screen size, resolution, features etc. Without any schema change, the products can store attributes relevant to each.

- MongoDB supports embedded documents, which allows customer reviews to be stored directly inside the product document. This makes it easy to retrieve a product along with all its reviews in a single query, improving performance.

- An RDBMS usually depends on one main server. This makes it difficult to handle very large workloads or recover quickly if that server fails, because it does not naturally support working across many servers. But MongoDB overcomes this issue as it is capable of scaling across multiple servers. 


## 3. Section C: Trade-offs 

### Question: What are two disadvantages of using MongoDB instead of MySQL for this product catalog?

### Answer:

- One disadvantage of using MongoDB instead of MySQL is weaker support for complex transactions. Although MongoDB supports transactions, relational databases like MySQL handle multi-table, ACID-compliant transactions more easily. In Fleximart, placing an order involves inserting order data, adding multiple order items, and updating product stock. MySQL manages these related steps reliably within a single transaction, ensuring consistency if any step fails.

- MongoDB also allows data duplication due to embedded documents, which can cause inconsistency if updates are missed. There is less data integrity enforcement in NoSQL databases. As MongoDB allows more data flexibility, data validation must be handled in application code, increasing the chance of inconsistent data.