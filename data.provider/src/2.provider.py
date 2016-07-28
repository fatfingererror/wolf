# provider.py usdchf 02

# argument 1 is a custom forex pair name
# argument 2 is a custom month number
import os
import sys, sched, time, calendar
from pytz import timezone
from datetime import datetime
from time import strftime
from kafka.client import KafkaClient
from kafka import KafkaProducer
from flask import json
from cassandra.cluster import Cluster

__here__ = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(__here__, '..', '..', 'histdata.com', 'data', 'csv')

schema = {
        "properties" : {
                "symbol" : {"type" : "string", "pattern" : "(AUDUSD)|(EURUSD)|(GBPUSD)|(NZDUSD)|(USDCAD)|(USDCHF)|(USDJPY)"},
                "issued_at" : {"type" : "number" },
                "bid" : {"type" : "number"},
                "ask" : {"type" : "number"},
        },
        "required": ["symbol", "issued_at", "bid", "ask"]
}

# connect to kafka
kafka_configs = os.getenv('KAFKA_PORT_9092_TCP').replace('tcp://', '')
kafka = KafkaClient(bootstrap_servers=[kafka_configs])
producer = KafkaProducer(bootstrap_servers=[kafka_configs])

db_configs = os.getenv('DATABASE_PORT_9042_TCP').replace('tcp://', '')
HOST, PORT = db_configs.split(':')
cluster = Cluster([HOST], port=PORT)
session = cluster.connect('wolf')


# time conversion and stuff
custom_month = -1
custom_day   = -1
est          = timezone('EST')

topic        = "forex"
topicJ       = "forexJ"

forex_pair   = "unknown"
if len(sys.argv) > 3:
    print(sys.argv)
    forex_pair = sys.argv[1]
    custom_year = sys.argv[2]
    custom_month = sys.argv[3]
    # custom_day = sys.argv[4]

# load a file to memory
# print "Loading data to memory..."
# lines = [line.strip() for line in sys.stdin]
# print "Loading data to memory done!"
filename = 'DAT_ASCII_' + forex_pair.upper() + '_T_' + custom_year + custom_month + '.csv'
path = os.path.join(DATA_DIR, filename)
# initialize scheduler
s = sched.scheduler(time.time, time.sleep)


def upload(q, m, l, j):
    print(m)
    producer.send(topic, str.encode(l))
    producer.send(topicJ, str.encode(j))
    session.execute(q)

print("Loading data to scheduler...")

with open(path) as f:
    for line in f:
        cols = line.split(",")
        date = cols[0].split(" ")

        year = date[0][0:4]
        month = date[0][4:6]
        if int(custom_month) > 0:
            month = custom_month
        day = date[0][6:8]
        # if custom_day>0:
                # day = custom_day

        hour = date[1][0:2]
        minute = date[1][2:4]
        second = date[1][4:6]
        milisec = date[1][6:9]

        bid = cols[1]
        ask = cols[2]

        timestring = year + month + day + hour + minute + second + milisec + "00"

        timezone_blind = datetime.strptime(timestring,"%Y%m%d%H%M%S%f")
        timezone_aware = est.localize(timezone_blind)
        utc_ts         = datetime.utctimetuple(timezone_aware)
        #utc_t          = mktime(utc_ts) + 1.0 * int(milisec) / 1000
        utc_t          = calendar.timegm(utc_ts) + 1.0 * int(milisec) / 1000
        utc_s1         = strftime('%Y-%m-%d %H:%M:%S.', utc_ts)
        utc_s1         = utc_s1 + milisec + "+0000"
        utc_k          = forex_pair + ":" + strftime('%Y-%m-%d', utc_ts)

        #print utc_ts
        #print utc_k

        q = "INSERT INTO ticks (pair_day,issued_at,bid,ask) VALUES ("
        q = q + "'" + utc_k + "',"
        q = q + "'" + utc_s1 + "',"
        q = q + "" + bid + ","
        q = q + "" + ask + ") USING TTL 10800;"

        m = "pushing " + forex_pair + " "
        m = m + utc_s1 + " "
        m = m + "to key " + utc_k + " "
        m = m + "with timestamp " + str(utc_t)

        tick  = forex_pair + " 0 " + '%d' % (utc_t * 1000) + " " + '%d' % (utc_t * 1000) + " " + str(bid) + " " + str(ask)
        tickJ = json.dumps({'symbol':forex_pair,'issued_at':utc_t,'bid':bid,'ask':ask})
        #validate(tickJ,schema)

        upload(q, m, tick, tickJ)

print("Loading data to scheduler done!")

# run the scheduler

print("Running scheduler...")
s.run()
print("Running scheduler done!")

# cleanup when scheduler is done
# cursor.close()
# con.close()
cluster.shutdown()
