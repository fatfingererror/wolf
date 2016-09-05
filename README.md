#Wolf
Trade foreign exchange with ease.

### Introduction
Wolf Trading Platform is an interactive platform that supports real-time financial data visualization, as well as historical data lookup. It executes simple trading rules in real time and is simple to integrate with the brokerage services. It is currently not deployed publicly. [Here](https://www.youtube.com/watch?v=0Q5XMwENRuY#t=23) and [here](https://www.youtube.com/watch?v=y7Gr5F1FHco&list=UU5KnJYd4JU21Qu8E8GgEexg) are screen casts from Wolf's operation.

Below is an overview of the architecture of Wolf:

![alt tag](https://raw.githubusercontent.com/slawekj/wolf/master/images/architecture.png "Architecture of Wolf")

Wolf uses the following modules:

  1. [Data Provider](data.provider/) (bottom box on the diagram above) is responsible for a real-time Forex feed to the system. To have that free of charge it uses data aggregated by [Hist Data](histdata.com) every month. The data feed is therefore one month old, e.g., a tick that happened in June at exactly '2014-06-03 15:32:21.451 EST' is fed to the system on July at exactly '2014-07-03 15:32:21.451 EST' (1 milisecond resolution). This approach helps generating traffic similar to what expensive data providers would provide. The downside is, apart from data being one-month old, the fact that a regular weekday in July might have been a weekend in June, which causes outage in feed.
  2. [Rule Submission](restful.rule.submission/) (top right box on the diagram above) is responsible for getting user-defined orders from investors. They are expressed as IF THEN statements, e.g. IF price of X is less than Y THEN buy X. Rules are delivered to the [Rule Engine](rule.engine/) and executed if the condition specified in the order is met. All rules enter the system via this API. [Web Interface](web.interface/) calls this API when user clicks to submit a rule.
  3. [Data Router](data.router/) (the second from the bottom box on the diagram above) is responsible for getting events generated by producers: "ticks" from [Data Provider](data.provider/) and orders from [Rule Submission](restful.rule.submission/) and deliver them to the appropriate consumers. It is built on top of [Kafka](https://kafka.apache.org/) distributed queue.
  4. [Rule Engine](rule.engine/) (the second left-most box on the diagram above) is one of the consumers of events provided by [Data Router](data.router/). It matches up rules with the current state of the market and executes the trades when the conditions specified in rules are met. It is built on top of [Storm](http://storm.incubator.apache.org/) event processor. The design of rule.engine is shown below: ![alt tag](https://raw.githubusercontent.com/slawekj/wolf/master/images/engine.png "Architecture of Rule Engine") There are two spouts: one provides ticks, one provides rules. It is a simple design, which matches up rules with ticks by the "symbol" field, e.g. it uses Storm field grouping. Execution bolt stores partially the latest state of the market, e.g. each task "knows" only about the state from the input ticks. Below is a run-time visualization of the topology running on Storm cluster: ![alt tag](https://raw.githubusercontent.com/slawekj/wolf/master/images/topology-runtime.png "Runtime visualization")
  5. [Data Aggregator - RT](data.aggregator.rt/) (the "Cassandra" box on the diagram above) is responsible for aggregating the latest ticks in real time. It is built on top of [Cassandra](http://cassandra.apache.org/) database. Ticks are only retained for 3 hours. This module takes advantage of the dynamic column families and TTL-tagged inserts, which is a mechanism of storing temporal time-series data in Cassandra.
  6. [Data Aggregator - Batch](data.aggregator.batch/) (the "HDFS" box on the diagram above) is responsible for storing all the incoming events in the system, aggregating a wide range of ticks in batch, averaging them, and serving aggregated views to [Data Aggregator - RT](data.aggregator.rt/). It is built on top of [HDFS](http://hadoop.apache.org/docs/r1.2.1/hdfs_design.html), [Camus](https://github.com/linkedin/camus), and [Hive](https://hive.apache.org/). Ticks are stored in HDFS every 10 minutes by Camus data collector. Camus creates a set of compressed files, groups them by hours, each line in such a file is one serialized json object representing a tick. A Hive table is defined over the directory that contains the files from the last hour, files are decompressed on-the-fly, json objects get flatten, average prices within every minute are calculated and sent to [Data Aggregator - RT](data.aggregator.rt/).
  7. [Cache - RT](restful.cache.service.rt/) ("restful cache" box on the diagram above) separates queries to the [Data Aggregator - RT](data.aggregator.rt/) from clients. It uses in-memory cache to serve requests in real time. [Cache - Batch](restful.cache.service.batch/) works exactly like [Cache - RT](restful.cache.service.rt/) but for the other types of queries. The distinction have been made between these modules because they are likely to be queried at different rates, e.g. [Cache - RT](restful.cache.service.rt/) is queried more frequently to give user the best possible experience, whereas [Cache - Batch](restful.cache.service.batch/) is queried less frequently because it depends on the data from [Data Aggregator - Batch](data.aggregator.batch/), serving every 10 minutes or so.
  8. [Web Interface](web.interface/) is a front-end that a regular investor can use to analyze Forex market and order trades. It is built on top of [Flot](http://www.flotcharts.org/) JavaScript graphing library. There are all the seven main Forex pairs plotted real-time on the main page of the system:
![alt tag](https://raw.githubusercontent.com/slawekj/wolf/master/images/plots-all.png "Main Page")
User can specify a trading rule in the bottom right corner of the system. Specifying URL is the way to link Wolf platform to the brokerage service. User can also click on any of the plots to see the historical data visualization:
![alt tag](https://raw.githubusercontent.com/slawekj/wolf/master/images/plot-detailed.png "Detailed Graph")
The top plot shows the latest minute of trade. The bottom plot shows the last hour, with values averaged per-minute in [Aggregator - Batch](data.aggregator.batch/) module. Note that the last couple of minutes are missing because MR jobs, executed by Hive, are running in background.

```
Modules should be deployed, possibly to different physical machines/clusters, in the following order:
  1. data.router (deployment scripts ready)
  2. data.provider (deployment scripts ready)
  3. rule.engine (deployment scripts ready)
  4. data.aggregator.rt (deployment scripts in preparation)
  5. data.aggregator.batch (deployment scripts in preparation)
  6. restful.cache.rt (deployment scripts in preparation)
  7. restful.cache.batch (deployment scripts in preparation)
  8. restful.rule.submission (deployment scripts in preparation)
  9. web.interface (deployment scripts in preparation)
```
