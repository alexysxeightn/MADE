from operator import add
import re

from pyspark import SparkConf, SparkContext


PATH_TO_WIKI_DUMP = "hdfs:///data/wiki/en_articles_part/"
WORD = "narodnaya"

spark_conf = (
    SparkConf()
    .set("spark.ui.port", 22117)
    .set("spark.driver.memory", "512m")
    .set("spark.executor.instances", "2")
    .set("spark.executor.cores", "1")
    .setAppName("alexysxeightn")
    .setMaster("yarn")
)
sc = SparkContext(conf=spark_conf)

wiki_rdd = sc.textFile(PATH_TO_WIKI_DUMP)

words_rdd = (
    wiki_rdd
    .map(lambda x: x.split("\t", 1))
    .map(lambda pair: pair[1].lower())
    .map(lambda text: re.findall(r"\w+", text))
    .flatMap(lambda x: zip(x, x[1:]))
    .filter(lambda bigram: bigram[0] == WORD)
    .map(lambda bigram: (f"{bigram[0]}_{bigram[1]}", 1))
    .reduceByKey(add)
    .sortByKey()
)

for bigram, cnt in words_rdd.collect():
    print(bigram, cnt, sep="\t")

sc.stop()
