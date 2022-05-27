import argparse
from pyspark import SparkContext
from pyspark.sql.functions import col, split
from pyspark.sql.session import SparkSession


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka-brokers", required=True)
    parser.add_argument("--topic-name", required=True)
    parser.add_argument("--starting-offsets", default='latest')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--processing-time", default='0 seconds')
    group.add_argument("--once", action='store_true')

    args = parser.parse_args()
    if args.once:
        args.processing_time = None
    else:
        args.once = None

    return args


def main(args):
    input_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", args.kafka_brokers) \
        .option("subscribe", args.topic_name) \
        .option("startingOffsets", args.starting_offsets) \
        .load()

    df = input_df.selectExpr("cast(value as string)")
    df = df.select(
        split(col("value"), '\t').getItem(1).alias("uid"),
        split(col("value"), '\t').getItem(2).alias("url"),
    )
    df.createOrReplaceTempView("page_views")

    res = spark.sql("""
        SELECT
            parse_url(url, 'HOST') as domain,
            COUNT(uid) as view,
            approx_count_distinct(uid) as unique
        FROM
            page_views
        GROUP BY
            domain
        ORDER BY
            view DESC
        LIMIT
            10
    """)

    query = res \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .trigger(once=args.once, processingTime=args.processing_time) \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()


if __name__ == '__main__':
    sc = SparkContext()
    spark = SparkSession(sc)
    spark.sparkContext.setLogLevel('WARN')
    spark.conf.set("spark.sql.shuffle.partitions", 5)

    args = parse_arguments()
    main(args)

    sc.stop()
