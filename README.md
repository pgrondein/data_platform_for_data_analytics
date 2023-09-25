# Data Platform for retail Data Analytics

This project goal is to design a Data Platform for retail Data Analytics. 

We will use MySQL as an OLTP database and MongoDB as a NoSQL database, design and implement a data warehouse and generate reports from the data, design a reporting dashboard that reflects the key metrics of the business, extract data from OLTP and NoSQL databases, transform it and load it into the data warehouse, then create an ETL pipeline, and finally, create a Spark connection to the data warehouse and then deploy a machine learning model.

Let’s go.

## Design of a OLTP database - MySQL

The first step is the design the OLTP database for an e-commerce website, populate the OLTP Database with the data provided, and automate the export of the daily incremental data into the data warehouse.

OLTP database is generally used to handle every day business transactions of an organization like a bank or a super market chain. OLTP databases can be write heavy or may have a balanced read/write load.

It is expected to handle a huge number of transactions per second. Each transaction usually involves accessing (read/write) a small portion of the database, in other words the payload per transaction is small. 

The time taken to execute a transaction usually called latency needs to be very less.

The schema of an OLTP database is higly normalized so as to achieve a very low latency. To further improve the latency an OLTP database stores only the recent data like the last few week's data. They are usually run on storage that is very fast like SSD.

The SQL queries can be found here : oltp_database_mysql.sql

