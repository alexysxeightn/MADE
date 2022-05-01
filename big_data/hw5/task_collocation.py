from operator import add
import re
from math import log

from pyspark import SparkConf, SparkContext


PATH_TO_WIKI_DUMP = "hdfs:///data/wiki/en_articles_part/"
PATH_TO_STOP_WORDS = "hdfs:///data/stop_words/stop_words_en-xpo6.txt"
TOP = 39
BIGRAMS_FILTER = 500

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
stopwords_rdd = sc.textFile(PATH_TO_STOP_WORDS)
stopwords_broadcast = sc.broadcast(stopwords_rdd.collect())

text_rdd = (
    wiki_rdd
    .map(lambda x: x.split("\t", 1))
    .map(lambda pair: pair[1].lower())
    .map(lambda text: re.findall(r"\w+", text))
    .map(lambda words: [word for word in words if word not in stopwords_broadcast.value])
)
text_rdd.cache()

words_rdd = (
    text_rdd
    .flatMap(lambda words: [(word, 1) for word in words])
)
words_rdd.cache()

pairs_rdd = (
    text_rdd
    .flatMap(lambda x: zip(x, x[1:]))
    .map(lambda bigram: (f"{bigram[0]}_{bigram[1]}", 1))
)
pairs_rdd.cache()

total_number_of_words = words_rdd.count()
total_number_of_word_pairs = pairs_rdd.count()

words_proba_rdd = (
    words_rdd
    .reduceByKey(add)
    .map(lambda x: (x[0], x[1] / total_number_of_word_pairs))
)
words_proba_rdd.cache()

pairs_proba_rdd = (
    pairs_rdd
    .reduceByKey(add)
    .filter(lambda x: x[1] >= BIGRAMS_FILTER)
    .map(lambda x: (x[0], x[1] / total_number_of_word_pairs))
)
pairs_proba_rdd.cache()

a_word_rdd = (
    pairs_proba_rdd
    .map(lambda x: (x[0].split("_")[0], (x[0], x[1])))
    .join(words_proba_rdd)
    .map(lambda x: (x[1][0][0], (x[1][0][1], x[1][1])))
)
b_word_rdd = (
    pairs_proba_rdd
    .map(lambda x: (x[0].split("_")[1], (x[0], x[1])))
    .join(words_proba_rdd)
    .map(lambda x: (x[1][0][0], x[1][1]))
)

npmi_fn = lambda p_ab, p_a, p_b: round(-log(p_ab / p_a / p_b) / log(p_ab), 3)

npmi_list = (
    a_word_rdd
    .join(b_word_rdd)
    .map(lambda x: (x[0], npmi_fn(x[1][0][0], x[1][0][1], x[1][1])))
    .takeOrdered(TOP, key=lambda x: -x[1])
)

for pair, npmi in npmi_list:
    print(pair, npmi, sep="\t")

sc.stop()
