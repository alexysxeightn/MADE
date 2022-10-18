HADOOP_STREAMING_JAR=/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar
INPUT=/AB_NYC_2019.csv

hdfs dfs -rm -r -skipTrash /mean_mapreduce
hdfs dfs -rm -r -skipTrash /var_mapreduce

yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name=mean_mapreduce \
	-files mapper_mean.py,reducer_mean.py \
	-mapper "./mapper_mean.py" \
	-reducer "./reducer_mean.py" \
	-input $INPUT \
	-output /mean_mapreduce

yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name=var_mapreduce \
	-files mapper_var.py,reducer_var.py \
	-mapper "./mapper_var.py" \
	-reducer "./reducer_var.py" \
	-input $INPUT \
	-output /var_mapreduce

hdfs dfs -cat /mean_mapreduce/part-00000
hdfs dfs -cat /var_mapreduce/part-00000