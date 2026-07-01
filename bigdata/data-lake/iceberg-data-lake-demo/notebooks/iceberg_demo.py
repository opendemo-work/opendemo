from pyspark.sql import SparkSession

spark = SparkSession.builder     .appName("IcebergDemo")     .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog")     .config("spark.sql.catalog.demo.type", "hadoop")     .config("spark.sql.catalog.demo.warehouse", "/data/warehouse")     .getOrCreate()

spark.sql("CREATE TABLE demo.orders (id BIGINT, amount DOUBLE, ts TIMESTAMP) USING iceberg PARTITIONED BY (days(ts))")
spark.sql("INSERT INTO demo.orders VALUES (1, 100.0, TIMESTAMP '2026-06-01 10:00:00')")
spark.sql("SELECT * FROM demo.orders").show()

# 时间旅行
spark.sql("SELECT * FROM demo.orders VERSION AS OF 1").show()
