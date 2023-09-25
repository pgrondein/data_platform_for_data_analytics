# This program requires the python module mysql-connector-python to be installed.
# Install it using the below command
# pip3 install mysql-connector-python

# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to PostgreSql
import psycopg2

# Connect to MySQL
connection = mysql.connector.connect(user = 'root', 
																		 password = 'PASSWORD',
																		 host = '127.0.0.1',
																		 database = 'sales')

# Connect to DB2 or PostgreSql
dsn_hostname = '127.0.0.1'
dsn_user = 'postgres' 
dsn_pwd = 'PASSWORD' 
dsn_port = "5432"               
dsn_database = "postgres"          

# Create connection
conn = psycopg2.connect(
   database = dsn_database, 
   user = dsn_user,
   password = dsn_pwd,
   host = dsn_hostname, 
   port = dsn_port
)

# Find out the last rowid from PostgreSql data warehouse
# The function get_last_rowid returns the last rowid of the table sales_data on the PostgreSql database.

def get_last_rowid():
    cursor = conn.cursor()
    cursor.execute("select MAX(rowid) from sales_data;");
    return cursor.fetchone()

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records returns a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    cursor = connection.cursor()
    SQL = """ SELECT * FROM sales_data WHERE rowid > %s; """
    cursor.execute(SQL, rowid);
    return cursor.fetchall()


new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records)

# Insert the additional records from MySQL into PostgreSql data warehouse.
# The function insert_records inserts all the records passed to it into the sales_data table in PostgreSql.

def insert_records(records):
    for row in records:
        cursor = conn.cursor()
        SQL = "INSERT INTO sales_data(rowid,product_id,customer_id,quantity) values(%s,%s,%s,%s)"
        cursor.execute(SQL,row);
        conn.commit()


insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# Disconnect from mysql warehouse
connection.close()

# Disconnect from DB2 or PostgreSql data warehouse 
conn.close()

# End of program
