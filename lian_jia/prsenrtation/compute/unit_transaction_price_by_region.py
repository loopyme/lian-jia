from pyspark import Row
from pyspark.sql import SparkSession

from lian_jia.config import DATA_DIR
from lian_jia.prsenrtation.config import MYSQL_CONN, conn_param

spark = (
    SparkSession.builder.appName("Python Spark SQL basic example")
        .config("spark.some.config.option", "some-value")
        .getOrCreate()
)
sc = spark.sparkContext

company_rdd = sc.textFile(str((DATA_DIR / "house_info" / "chengjiao.csv").absolute()))


def to_pair(item):
    items = item.split(",")
    price, region = items[-5], items[-1]

    try:
        price = float(price)
    except Exception as _:
        price = 0

    return region, price


pair_rdd = (
    company_rdd.map(lambda x: to_pair(x))
        .reduceByKey(lambda x, y: x + y)
        .map(lambda x: Row(region=x[0], amount=x[1]))
)
schema_bank = spark.createDataFrame(pair_rdd)

schema_bank.write.jdbc(MYSQL_CONN, "unit_transaction_price_by_region", "overwrite", conn_param)
print("Done: unit_transaction_price_by_region")
