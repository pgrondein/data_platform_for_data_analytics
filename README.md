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

![softcartRelationships](https://github.com/pgrondein/data_platform_for_data_analytics/assets/113172845/e27177e3-9134-4f59-8e0f-dc12a0168dfc)


We then generate the SQL script from the ERD design tool to optain the data warehouse schema. 

After loading data into the different tables, we write aggregation queries and create MQTs to make reporting easier.

- Grouping sets query using the columns country, category, totalsales, to get total sales per country and category
  
```SQL
SELECT country, category, sum(amount) AS totalsales
FROM factsales
LEFT JOIN dimcountry
ON factsales.countryid = dimcountry.countryid
LEFT JOIN dimcategory
ON factsales.categoryid = dimcategory.categoryid
GROUP BY GROUPING SETS(country,category)
ORDER BY country, category
```
- Rollup query using the columns year, country, and totalsales, to get total sales per year and country

```sql
SELECT year, country, sum(amount) AS totalsales
FROM factsales
LEFT JOIN dimdate
ON factsales.dateid = dimdate.dateid
LEFT JOIN dimcountry
ON factsales.countryid = dimcountry.countryid
GROUP BY ROLLUP(year,category)
ORDER BY year, country
```

- cube query using the columns year, country, and average sales, to get the average sales per year and country

```sql
SELECT year, country, avg(amount) AS averagesales
FROM factsales
LEFT JOIN dimdate
ON factsales.dateid = dimdate.dateid
LEFT JOIN dimcountry
ON factsales.countryid = dimcountry.countryid
GROUP BY CUBE(year,category)
ORDER BY year, country
```

- MQT named total_sales_per_country that has the columns country and total_sales.

```sql
CREATE TABLE total_sales_per_country(country, totalsales) AS
		(SELECT country, sum(amount)
FROM factsales
LEFT JOIN dimcountry
ON factsales.countryid = dimcountry.countryid
GROUP BY country)
		DATA INITIALLY DEFERRED
		REFRESH DEFERRED
		MAINTAINED BY SYSTEM;
```

## Design of a Business Intelligence Dashboard - IBM Cognos Analytics

We will create a bar chart of quarterly sales of cell phones, create a pie chart of sales of electronic goods by category, and create a line chart of total sales per month for a given year.

### Bar chart of quarterly sales of cell phones

![barchart](https://github.com/pgrondein/data_platform_for_data_analytics/assets/113172845/1cb8f732-7e89-4d3a-951d-3ea53a45dbf0)

### Pie chart of sales of electronic goods by category

![piechart](https://github.com/pgrondein/data_platform_for_data_analytics/assets/113172845/1539299a-27d7-4eae-8b61-5c5c734eda59)

### Line chart of total sales per month for a given year

![linechart](https://github.com/pgrondein/data_platform_for_data_analytics/assets/113172845/4c9abae2-c962-4c04-9944-7643d08efa08)

## Design of an ETL - MySQL/PostgreSQL

As Data Engineer, we need to keep data synchronized between different databases/data warehouses as a part of your daily routine. One task that is routinely performed is the sync up of staging data warehouse and production data warehouse. Automating this sync up will save you a lot of time and standardize your process. 

We will write python scripts to perform incremental data load from MySQL and PostgreSQL server which acts as a staging warehouse to the PostgreSQL which is a production data warehouse. This script will be scheduled by the data engineers to sync up the data between the staging and production data warehouse.

The Python script needs to 

- connect to PostgreSQL data warehouse and identify the last row on it.
- connect to MySQL staging data warehouse and find all rows later than the last row on the datawarehouse.
- Insert the new data in the MySQL staging data warehouse into the PostgreSQL production data warehouse.

The Python script is available here : [etl.py](https://github.com/pgrondein/data_platform_for_data_analytics/blob/f1cf0e857b2209264bfe97486afc96dcc1e491a6/etl.py)


