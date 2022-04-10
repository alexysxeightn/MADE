set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
NUM_REDUCERS=5

hdfs dfs -rm -r -skipTrash $2*

yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name=$3 \
	-files mapper.py,reducer.py \
	-mapper "mapper.py" \
	-reducer "reducer.py" \
	-numReduceTasks $NUM_REDUCERS \
	-input $1 \
	-output $2

hdfs dfs -cat $2/part-00000 | head -n 50