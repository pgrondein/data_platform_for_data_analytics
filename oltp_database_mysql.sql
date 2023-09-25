-- Create the database
create database sales;
-- Connect to the database
use sales;

-- Define a table
CREATE TABLE sales_data (product_id INTEGER NOT NULL, 
			customer_id INTEGER NOT NULL, 
			price INTEGER, 
			quantity INTEGER, 
			timestamp_ DATETIME);

-- Show all tables in database sales
SHOW FULL TABLES WHERE table_type = 'BASE TABLE';

-- Find out the count of records in the tables sales_data
SELECT COUNT(*) FROM sales_data;

-- Create an index named ts on the timestamp field
CREATE UNIQUE INDEX ts ON sales_data(timestamp_);

-- List indexes on the table sales_data.
SHOW INDEXES FROM sales_data;
