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

The OLTP database schema can be found here : [oltp_database_mysql.sql](https://github.com/pgrondein/data_platform_for_data_analytics/blob/ea1e2ab4eb97e72ba43c80f5660b7042c1edb92b/oltp_database_mysql.sql)

The bash script to export data can be found here : [datadump.sh](https://github.com/pgrondein/data_platform_for_data_analytics/blob/275c7240d5176d47dbfe530c89684cb99ee3c20e/datadump.sh)

## Design of a NoSQL database - MongoDB

We will set up a NoSQL database to store the catalog data for the E-website, load the E-Commerce catalog data into the NoSQL database, and query the E-Commerce catalog data in the NoSQL database

We need the ‘mongoimport’ and ‘mongoexport’ tools to move data in and out of the mongodb database. To install these tools run the below commands on the terminal.

'''powershell
wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
tar -xf mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
export PATH=$PATH:/home/project/mongodb-database-tools-ubuntu1804-x86_64-100.3.1/bin
echo "done"
'''

