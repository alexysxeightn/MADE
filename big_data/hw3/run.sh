set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
NUM_REDUCERS=8

INPUT_IDS_HDFS_PATH=$1
OUTPUT_HDFS_PATH=$2
JOB_NAME=$3

hdfs dfs -rm -r -skipTrash ${OUTPUT_HDFS_PATH}*

( yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.name=$JOB_NAME \
    -D stream.num.map.output.key.fields=2 \
    -D stream.num.reduce.output.key.fields=2 \
    -D mapreduce.partition.keypartitioner.options=-k1.1,1.4 \
    -files mapper.py,reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -mapper 'mapper.py' \
    -reducer 'reducer.py' \
    -combiner 'reducer.py' \
    -numReduceTasks $NUM_REDUCERS \
    -input $INPUT_IDS_HDFS_PATH \
    -output ${OUTPUT_HDFS_PATH}_tmp &&

yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.name=$JOB_NAME \
    -D stream.num.map.output.key.fields=3 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options='-k1,1n -k3,3nr' \
    -file reducer_2.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -mapper cat \
    -reducer 'reducer_2.py' \
    -numReduceTasks 1 \
    -input ${OUTPUT_HDFS_PATH}_tmp \
    -output ${OUTPUT_HDFS_PATH} 
) || echo 'Error happens'

hdfs dfs -rm -r -skipTrash ${OUTPUT_HDFS_PATH}_tmp

hdfs dfs -cat ${OUTPUT_HDFS_PATH}/* | head -20