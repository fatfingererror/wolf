#!/usr/bin/python

import os, sys
from time import strftime
from datetime import datetime
from cassandra.cluster import Cluster

# connect to database
db_configs = os.getenv('DATABASE_PORT_9042_TCP').replace('tcp://', '')
HOST, PORT = db_configs.split(':')
cluster = Cluster([HOST], port=PORT)
session = cluster.connect('wolf')

for t in sys.stdin:
    f          = t.split('\t')
    pair       = f[0].strip()
    issued_at  = f[1].strip()
    bid        = f[2].strip()
    ask        = f[3].strip()

    utc_day    = datetime.fromtimestamp(float(issued_at)).strftime('%Y-%m-%d')
    utc_hour   = datetime.fromtimestamp(float(issued_at)).strftime('%Y-%m-%d %H:%M:%S+0000')

    q = "INSERT INTO ticks_avg_s (pair_day,issued_at,bid,ask) VALUES ("
    q = q + "'" + pair + ":" + utc_day + "',"
    q = q + "'" + utc_hour + "',"
    q = q + "" + bid + ","
    q = q + "" + ask + ") USING TTL 10800"

    m = "pushing " + pair + " "
    m = m + utc_hour + " "
    m = m + "to key " + pair + ":" + utc_day

    print(m)
    session.execute(q)


cluster.shutdown()
