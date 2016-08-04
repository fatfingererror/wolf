FROM ubuntu:14.04

# Environment
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV PROJECT_NAME data.aggregator.batch
ENV PROJECT_ROOT /srv/$PROJECT_NAME

WORKDIR $PROJECT_ROOT

ADD ./data.aggregator.batch $PROJECT_ROOT

# install openssh-server, openjdk and wget
RUN apt-get update && apt-get install -y openssh-server openjdk-7-jdk wget
RUN apt-get install -y build-essential python3.4 python3-pip python3-dev
RUN pip3 install --upgrade pip && pip install --no-cache-dir --upgrade --force-reinstall -r hadoop-cluster-docker/requirements.txt

# Install hadoop 2.7.2
RUN wget https://github.com/kiwenlau/compile-hadoop/releases/download/2.3.0/hadoop-2.3.0.tar.gz && \
    tar -xzvf hadoop-2.3.0.tar.gz && \
    mv hadoop-2.3.0 /usr/local/hadoop && \
    rm hadoop-2.3.0.tar.gz

# Install Gradle
RUN wget https://github.com/linkedin/gobblin/releases/download/gobblin_0.7.0/gobblin-distribution-0.7.0.tar.gz && \
    tar -xzvf gobblin-distribution-0.7.0.tar.gz && \
    mv gobblin-dist /usr/local/gobblin && \
    rm gobblin-distribution-0.7.0.tar.gz

ENV GOBBLIN_HOME=/usr/local/gobblin
ENV PATH=$PATH:$GOBBLIN_HOME/bin
RUN mkdir $GOBBLIN_HOME/fin
RUN mkdir $GOBBLIN_HOME/fout
ENV GOBBLIN_WORK_DIR /usr/local/gobblin/fout
ENV GOBBLIN_JOB_CONFIG_DIR /usr/local/gobblin/fin


# set environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_BIN_DIR=$HADOOP_HOME/bin
ENV PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

RUN mkdir -p ~/hdfs/namenode && \
    mkdir -p ~/hdfs/datanode && \
    mkdir $HADOOP_HOME/logs

RUN mv $PROJECT_ROOT/hadoop-cluster-docker/config/ssh_config ~/.ssh/config && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    # m$PROJECT_ROOTmhadoop-cluster-docker/config/p/slaves $HADOOP_HOME/etc/hadoop/slaves && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/start-hadoop.sh ~/start-hadoop.sh && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/run-wordcount.sh ~/run-wordcount.sh && \
    mv $PROJECT_ROOT/hadoop-cluster-docker/config/kafka.pull $GOBBLIN_HOME/fin/kafka.pull

RUN chmod +x ~/start-hadoop.sh && \
    chmod +x ~/run-wordcount.sh && \
    chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh

# format namenode
RUN /usr/local/hadoop/bin/hdfs namenode -format

CMD [ "sh", "-c", "service ssh start; bash"]
