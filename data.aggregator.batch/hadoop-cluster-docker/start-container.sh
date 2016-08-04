#!/bin/bash

# the default node number is 3
N=${1:-3}


# start hadoop master container
# containers running on different networks (--net) cannot be linked properly
docker rm -f hadoop-master &> /dev/null
echo "start hadoop-master container..."
docker run -itd -p 50070:50070 -p 8088:8088 --name hadoop-master --hostname hadoop-master --link wolf_cassandra_1:database --link wolf_data_router_1:kafka wolf_hadoop &> /dev/null

# start hadoop slave container
# i=1
# while [ $i -lt $N ]
# do
# 	 docker rm -f hadoop-slave$i &> /dev/null
# 	 echo "start hadoop-slave$i container..."
# 	 docker run -itd \
# 	                --net=hadoop \
# 	                --name hadoop-slave$i \
# 	                --hostname hadoop-slave$i \
# 	                kiwenlau/hadoop:1.0 &> /dev/null
# 	 i=$(( $i + 1 ))
# done

# get into hadoop master container
docker exec -it hadoop-master bash
