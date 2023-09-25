!pip install pyspark
!pip install findspark
!pip install pandas

import findspark
findspark.init()

import pyspark
print(pyspark.__version__)

import pandas as pd
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

# Creating a spark context class
sc = SparkContext()

# Creating a spark session
spark = SparkSession \
    .builder \
    .appName("Python Spark DataFrames basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

spark

# Load csv into a Spark dataframe
!curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/searchterms.csv >> searchterms.csv
sdf = spark.read.option("header",'True').option('delimiter', ',').csv("searchterms.csv")

# Print number of rows and columns
rows = sdf.count()
print(f"DataFrame Rows count : {rows}")
cols = len(sdf.columns)
print(f"DataFrame Columns count : {cols}")

# Print top 5 rows
sdf.show(5)

# Find out the datatype of the column searchterm
for col in sdf.dtypes:
    print(col[0]+" , "+col[1])
sdf.dtypes[3][1]

# How many times was the term gaming laptop searched
sdf.filter(sdf["searchterm"] == 'gaming laptop').count()

# Print the top 5 most frequently used search terms
sdf.groupBy('searchterm').count().orderBy('count', ascending=False).show(5)

# Load the sales forecast model
!curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/searchterms.csv >> searchterms.csv

# open file
file = tarfile.open('model.tar.gz')
  
# extracting file
file.extractall('./model')
file.close()

loaded_model = PipelineModel.load("./model/")

# Using the sales forecast model, predict the sales for the year of 2023
testing_data = sdf.filter(sdf["year"] == '2023')
predictions = loaded_model.transform(testing_data)
