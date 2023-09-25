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

```powershell
wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
tar -xf mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
export PATH=$PATH:/home/project/mongodb-database-tools-ubuntu1804-x86_64-100.3.1/bin
echo "done"
```
We verify that the tool got installed, by running the below command on the terminal.
```powershell
mongoimport --version
```
We import a document into a database named catalog and a collection named electronics in one command.
```powershell
mongoimport -u root -p MTY5Ni1wZ3JvbmRl --authenticationDatabase admin --db catalog --collection electronics --file catalog.json
```
Then we can start working with MongoDB.

```MongoDB
# List out all databases to check if catalog is here
show dbs

# List out all the collections in the database catalog
use catalog
show collections

# Creation of an index on the field "type"
db.electronics.createIndex({"type":1})

# Find the count of laptops
db.electronics.count({"type":"laptop"})

# Find the number of smart phones with screen size of 6 inches.
db.electronics.find({"type":"smart phone", "screen size": 6}).count()

# Find out the average screen size of smart phones.
db.electronics.aggregate([{"$match":{"type":"smart phone"}},{"$group":{"_id":"$type", "average":{"$avg":"$screen size"}}}])
```
We now export the fields _id, “type”, “model”, from the ‘electronics’ collection into a file named electronics.csv
```powershell
We now export the fields _id, “type”, “model”, from the ‘electronics’ collection into a file named electronics.csv
```
## Design & Build of a Data Warehouse - PostgreSQL

We will now design the schema for a data warehouse based on the schema of the OLTP and NoSQL databases. We’ll then create the schema and load the data into the fact and dimension tables, automate the daily incremental data insertion into the data warehouse, and create Cubes and Rollups to make the reporting easier.

The company retails download only items like E-Books, Movies, Songs etc. It has international presence and customers from all over the world, and would like to create a data warehouse so that it can create reports like

- total sales per year per country
- total sales per month per category
- total sales per quarter per country
- total sales per category per country

We use the ERD Design Tool of pgAdmin from PostgreSQL.

![softcartRelationships.jpg](https://prod-files-secure.s3.us-west-2.amazonaws.com/589f2cdb-c9de-4013-a992-6fb063ff1ea6/f098a2f9-1845-4a8b-8b53-e96f0387e141/softcartRelationships.jpg)




