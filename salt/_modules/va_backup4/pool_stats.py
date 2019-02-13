#!/usr/bin/env python
import rrdtool, datetime, time
from os import path

POOL_PATH = '/var/log/BackupPC/poolUsage.rrd'

def parse_pool_data(start = '-120d', interval = '60'):
    rrd_path = POOL_PATH
    rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE','--start', start, '-r', interval)
    start, end, resolution = rrd_info[0]
    rrd_rows = rrd_info[2]
    timestamp = start
    result = []
    for row in rrd_rows:
        x = timestamp
        x= str(datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'))
        y1= row[1]
        y2= row[4]
        if not y1 is None:
            result.append({'timestamp': x, 'full_size': round(y1/1024/1024*1.073741824), 'after_optimization':round(y2/1024/1024*1.073741824)})
        timestamp+= resolution

    return result
