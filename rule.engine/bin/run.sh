#!/bin/bash -e

# do I really need autopurge?
#sudo echo autopurge.purgeInterval=24 >> /etc/zookeeper/conf/zoo.cfg
#sudo echo autopurge.snapRetainCount=5 >> /etc/zookeeper/conf/zoo.cfg
sudo ./other/zookeeper-3.4.8/bin/zkServer.sh start

# check if zookeeper is running
echo stat | nc localhost 2181

# run nimbus
# ./apache-storm-0.9.2-incubating/bin/storm nimbus &
./other/storm/bin/storm nimbus &

sleep 10
# run storm ui
./other/apache-storm-1.0.1/bin/storm ui &
sleep 10
# run storm supervisor
./other/apache-storm-1.0.1/bin/storm supervisor &
sleep 10
# now build topology
./other/apache-storm-1.0.1/bin/storm jar ./wolf/rule.engine/target/rule.engine-0.0.1-SNAPSHOT-jar-with-dependencies.jar rule.engine.RuleEngineTopology RuleEngine

