#!/bin/bash

JAR=/usr/local/gobblin/build/gobblin-example/libs/gobblin-example-0.7.0.jar
CLASS=gobblin.example.simplejson.SimpleJsonExtractor
PROPERTIES=/usr/local/gobblin/gobblin-example/src/main/resources/simplejson.pull
HADOOP=hadoop

$HADOOP jar $JAR $CLASS -P $PROPERTIES

# For more
# http://gobblin.readthedocs.io/en/latest/case-studies/Kafka-HDFS-Ingestion/
