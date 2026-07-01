from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col

spark = SparkSession.builder     .appName("OpenDemo Spark SQL")     .master("spark://spark-master:7077")     .getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv("/data/sales.csv")
df.createOrReplaceTempView("sales")

result = spark.sql('''
    SELECT category, SUM(amount) as total_sales, AVG(amount) as avg_sales
    FROM sales
    GROUP BY category
    ORDER BY total_sales DESC
''')

result.show()
spark.stop()
