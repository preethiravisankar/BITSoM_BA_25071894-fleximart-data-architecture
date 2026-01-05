# FlexiMart Data Architecture Project

**Student Name:** Preethi Ravisankar  
**Student ID:** BITSoM_BA_25071894  
**Email:** preethiravisankar@gmail.com  
**Date:** 06.01.2026  

## Project Overview

This project involves building end-to-end pipeline for Fleximart - transforming raw csv data into analytics system that supports business reporting and decision-making. It includes creating an ETL pipeline, documenting a relational database, running business SQL queries, analyzing product data using MongoDB, and designing a star-schema data warehouse for analytical reporting.

## Repository Structure
├── part1-database-etl/  
│   ├── etl_pipeline.py  
│   ├── schema_documentation.md  
│   ├── business_queries.sql  
│   └── data_quality_report.txt  
├── part2-nosql/  
│   ├── nosql_analysis.md  
│   ├── mongodb_operations.js  
│   └── products_catalog.json  
├── part3-datawarehouse/  
│   ├── star_schema_design.md  
│   ├── warehouse_schema.sql  
│   ├── warehouse_data.sql  
│   └── analytics_queries.sql  
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

I gained hands-on experience in handling raw data and loading clean data into a relational database system. Also, to handle flexible data with varied attributes in a NoSQL database (MongoDB). Gained insight into how different data storage systems (RDBMS, NoSQL) work together in a real-world analytics pipeline.

## Challenges Faced

1. The customer and product datasets used character-based primary keys (such as C001 and P001), while the database tables were designed with auto-incremented integer primary keys. The sales dataset referenced these character-based customer_id and product_id values. To handle this mismatch, a temporary mapping was created to link the dataset IDs with the corresponding auto-generated database IDs during data insertion.
2. To handle rows with missing product_ids in the sales dataset, I matched the price values in the sales data with the corresponding prices in the products dataset to identify the correct product_ids. This approach was feasible because each product had a unique price, and the dataset size was small.
