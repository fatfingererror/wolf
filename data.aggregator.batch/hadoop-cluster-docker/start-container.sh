#!/bin/bash

# the default node number is 3
N=${1:-3}


# start hadoop master container
# containers running on different networks (--net) cannot be linked properly
# be careful with the links (they must refer to existing containers), docker does error
docker rm -f hadoop-master &> /dev/null
echo "start hadoop-master container..."
docker run -itd -p 50070:50070 -p 8088:8088 --name hadoop-master --net=hadoop  --hostname hadoop-master --link wolf_cassandra_1:database --link kafka wolf_hadoop &> /dev/null

# start hadoop slave container
i=1
while [ $i -lt $N ]
do
	 docker rm -f hadoop-slave$i &> /dev/null
	 echo "start hadoop-slave$i container..."
	 docker run -itd \
	                --name hadoop-slave$i \
                        --net=hadoop \
                        --link wolf_cassandra_1:database --link kafka \
	                --hostname hadoop-slave$i \
	                wolf_hadoop &> /dev/null
	 i=$(( $i + 1 ))
done

# get into hadoop master container
docker exec -it hadoop-master bash
