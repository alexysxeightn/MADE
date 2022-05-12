from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col

sc = SparkContext()
spark = SparkSession(sc)

DATA_PATH = 'hdfs:///data/twitter/twitter.txt'
FOLLOWER, USER = 12, 34

right = (
        spark
        .read
        .format('csv')
        .options(delimiter='\t', inferSchema=True)
        .load(DATA_PATH)
        .withColumnRenamed('_c0', 'user')
        .withColumnRenamed('_c1', 'follower')
)
left = right.filter(col('follower') == FOLLOWER).select(col('user'))

length = 0

while True:
    left.cache()
    left = left.withColumnRenamed('user', 'follower')
    length += 1
    if len(left.filter(col('follower') == USER).head(1)) > 0:
        break
    left = left.join(right, 'follower', 'inner').select(col('user'))

print(length)

sc.stop()
