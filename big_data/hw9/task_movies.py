import sys
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col, regexp_extract, regexp_replace, split, substring, trim
from pyspark.sql.types import IntegerType


PATH_TO_DATA = 'hdfs:///data/movielens/movies.csv'

sc = SparkContext()
spark = SparkSession(sc)

df = spark \
    .read \
    .format('csv') \
    .load(PATH_TO_DATA, sep=',', header=True)

df2 = df \
    .filter(col('genres') != '(no genres listed)') \
    .select(
        df.movieId.cast(IntegerType()) \
        .alias('movieid'),

        trim(regexp_replace(df.title, r'\(\d+\)', '')) \
        .alias('title'),
        
        substring(regexp_extract(df.title, r'\(\d\d\d\d\)', 0), 2, 4).cast(IntegerType()) \
        .alias('year'),
        
        split(trim(df.genres), pattern='\|') \
        .alias('genres')
    ) \
    .filter(col('year').isNotNull())

df2 \
    .write \
    .format('org.apache.spark.sql.cassandra') \
    .options(table='movies', keyspace=sys.argv[1]) \
    .mode('append') \
    .save()

sc.stop()