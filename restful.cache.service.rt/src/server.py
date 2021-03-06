#!/usr/bin/python
import os
from flask import Flask, jsonify
import threading
import time, datetime
import socket
from flask import make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
from cassandra.cluster import Cluster

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# connect to database
db_configs = os.getenv('DATABASE_PORT_9042_TCP').replace('tcp://', '')
HOST, PORT = db_configs.split(':')
cluster = Cluster([HOST], port=PORT)
session = cluster.connect('wolf')

tasks = {
    'AUDUSD':0,
    'EURUSD':0,
    'GBPUSD':0,
    'NZDUSD':0,
    'USDCAD':0,
    'USDCHF':0,
    'USDJPY':0
}

pairs = ['AUDUSD', 'EURUSD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY']

q = "select issued_at, ask, bid from ticks where pair_day = '%s' and issued_at > '%s'"

def foo(pairs):
    while True:
        for p in pairs:
            date = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)

            today = str(date.year) + "-" + str(date.month).zfill(2) + "-" + str(date.day).zfill(2)
            key   = p + ":" + today
            utc = today + " " + str(date.hour).zfill(2) + ":" + str(date.minute).zfill(2)
            utc = utc + ":" + str(date.second).zfill(2) + "+0000"

            data = session.execute(q % (key, utc))
            # print(q % (key, utc))

            #workaround
            # print("got " + str(len(data)) + " results from DB for " + p)
            tasks[p] = []
            for d in data:
                # print(d)
                # d[0] = str(datetime.datetime.fromtimestamp(
                    # struct.unpack('!Q', d[0])[0]/1e3 )
                # )
                tasks[p].append(d)

        time.sleep(2)

threading.Thread(target=foo, args=(pairs,)).start()

app = Flask(__name__)

#app.config["CACHE_TYPE"] = "null"
#print app.config['CACHE_TYPE']

@app.route('/', methods = ['GET'])
@crossdomain(origin='*')
def get_tasks():
    return jsonify( { 'ticks': tasks } )

if __name__ == '__main__':
    app.debug = True
    host=socket.gethostbyname(socket.gethostname())
    app.run(host=host)
    # cluster.shutdown()
