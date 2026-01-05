-- Database: fleximart_dw
-- CREATE DATABASE fleximart_dw;
USE fleximart_dw;
-- =========================
-- DIM DATE (30 dates: Jan–Feb 2024)
-- =========================
INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,false),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,false),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,false),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,false),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,false),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,true),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,true),

(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,false),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,false),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,false),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,true),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,true),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,false),
(20240116,'2024-01-16','Tuesday',16,1,'January','Q1',2024,false),
(20240117,'2024-01-17','Wednesday',17,1,'January','Q1',2024,false),

(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,false),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,false),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,false),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,false),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,true),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,true),
(20240212,'2024-02-12','Monday',12,2,'February','Q1',2024,false),
(20240213,'2024-02-13','Tuesday',13,2,'February','Q1',2024,false),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,false),
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,false);

-- select * from dim_date;

-- =========================
-- DIM PRODUCT (15 products, 3 categories)
-- =========================
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001','Laptop','Electronics','Computers',75000),
('P002','Smartphone','Electronics','Mobiles',45000),
('P003','Headphones','Electronics','Accessories',3000),
('P004','Smart TV','Electronics','Television',55000),
('P005','Bluetooth Speaker','Electronics','Audio',5000),

('P006','Men T-Shirt','Clothing','Men Tops',1200),
('P007','Women Dress','Clothing','Women Wear',3500),
('P008','Jeans','Clothing','Bottom Wear',2500),
('P009','Jacket','Clothing','Outerwear',6000),
('P010','Kids Wear Set','Clothing','Kids Wear',1800),

('P011','Running Shoes','Footwear','Sports Shoes',4200),
('P012','Formal Shoes','Footwear','Office Wear',5200),
('P013','Sandals','Footwear','Casual Wear',2200),
('P014','Sneakers','Footwear','Casual Shoes',4800),
('P015','Flip Flops','Footwear','Slippers',900);

-- select * from dim_product;

-- =========================
-- DIM CUSTOMER (12 customers, 4 cities)
-- =========================
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','John Doe','Mumbai','Maharashtra','Premium'),
('C002','Anita Sharma','Bengaluru','Karnataka','Regular'),
('C003','Rahul Verma','Delhi','Delhi','Regular'),
('C004','Sneha Iyer','Chennai','Tamil Nadu','Premium'),
('C005','Amit Patel','Ahmedabad','Gujarat','Regular'),
('C006','Neha Singh','Mumbai','Maharashtra','New'),
('C007','Karthik R','Bengaluru','Karnataka','Premium'),
('C008','Pooja Mehta','Delhi','Delhi','Regular'),
('C009','Rohan Das','Chennai','Tamil Nadu','New'),
('C010','Simran Kaur','Mumbai','Maharashtra','Regular'),
('C011','Vikram Rao','Bengaluru','Karnataka','Premium'),
('C012','Meena N','Ahmedabad','Gujarat','Regular');

-- select * from dim_customer;

-- =========================
-- FACT SALES (40 transactions)
-- Higher volume on weekends, varied quantities
-- =========================
INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES

(20240106,1,1,2,75000,5000,145000),
(20240107,2,2,1,45000,2000,43000),
(20240107,11,3,3,4200,600,12000),
(20240113,6,4,4,1200,0,4800),
(20240114,14,5,2,4800,300,9300),

(20240115,3,6,1,3000,0,3000),
(20240116,7,7,2,3500,500,6500),
(20240117,10,8,1,1800,0,1800),

(20240203,4,9,1,55000,5000,50000),
(20240203,12,10,2,5200,400,10000),
(20240204,9,11,1,6000,500,5500),
(20240204,15,12,5,900,0,4500),

(20240210,5,1,2,5000,300,9700),
(20240210,8,2,1,2500,0,2500),
(20240211,13,3,3,2200,200,6400),
(20240211,6,4,2,1200,0,2400),

(20240212,1,5,1,75000,0,75000),
(20240213,2,6,2,45000,4000,86000),
(20240214,7,7,1,3500,0,3500),
(20240215,11,8,2,4200,300,8100),

(20240110,3,9,2,3000,200,5800),
(20240111,4,10,1,55000,0,55000),
(20240112,6,11,3,1200,0,3600),
(20240113,7,12,2,3500,300,6700),

(20240114,14,1,1,4800,0,4800),
(20240115,15,2,4,900,0,3600),
(20240116,10,3,2,1800,0,3600),
(20240117,8,4,1,2500,0,2500),

(20240205,12,5,1,5200,200,5000),
(20240206,9,6,1,6000,0,6000),
(20240207,13,7,2,2200,0,4400),
(20240208,11,8,3,4200,600,12000),

(20240209,6,9,2,1200,0,2400),
(20240210,7,10,1,3500,0,3500),
(20240211,1,11,1,75000,3000,72000),
(20240212,2,12,2,45000,5000,85000),

(20240210, 2, 3, 1, 45000, 2000, 43000),   
(20240211, 11, 6, 2, 4200, 400, 8000),  
(20240116, 6, 9, 3, 1200, 0, 3600),      
(20240205, 15, 10, 5, 900, 0, 4500);      

-- select * from fact_sales;