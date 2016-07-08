#!/bin/bash -e

# remove all previous java
# apt-get purge openjdk-\* icedtea-\* icedtea6-\*

# install java 1.7
# apt-get install -y openjdk-7-jre

# apt-get install zookeeper
# zookeeper conf is in /etc/zookeeper/conf/zoo.cfg

cd wolf/rule.engine && mvn clean install
