#!/usr/bin/env python
# import xml.etree.ElementTree as ET
import rrdtool, datetime, time
from os import path

POOL_PATH = '/var/log/BackupPC/poolUsage.rrd'

def parse_pool_data(start = '-4w', interval = '60'):
    rrd_path = POOL_PATH
    rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE','--start', start, '-r', interval)
    start, end, resolution = rrd_info[0]
    # labels = ['-','Full Size','-','-','After compression/deduplication']
    # units = ['-' ,'bytes','-','-', 'bytes']
    rrd_rows = rrd_info[2]
    # return rrd_rows
    # data = {}
    #return units
    # index=0

    timestamp = start
    result = []
    for row in rrd_rows:
        x = timestamp
        x= str(datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'))
        y1= row[1]
        y2= row[4]

        if not y1 is None:
            result.append({'timestamp': x, 'full_size': y1/1024/1024, 'after_optimization':y2/1024/1024})
        timestamp+= resolution



    # for label_index, label in enumerate(labels): # we want a separate graph for every label
    #     if index in [1,4]:
    #         timestamp = start
    #         if units[index]:
    #             units[index].replace('%%','%')
    #             label_unit = labels[index]+' ('+units[index]+')'
    #         else:
    #             label_unit = labels[index]
    #         result = []
    #         for row in rrd_rows:
    #             x = timestamp
    #             x= str(datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M'))
    #             y = row[label_index]

    #             # if y is None: y = float('nan')
    #             if not y is None:
    #                 result.append({'x': x, 'y': y, 'label_unit':label_unit})
    #             timestamp+= resolution

    #         data[label_unit] = result
    #     index=index +1
    return result

# def parse(host, service, start = '-1h', interval = '60'):
#     return parse_pnp_data(host, service, start, interval)

# def parse_get_table(host, service, start = '-1h', interval = '60'):
#     pnp_data = parse_pnp_data(host, service, start, interval)
#     pnp_data = [{'ts' : i['x'], key : i['y']} for key in pnp_data for i in pnp_data[key]]
#     return pnp_data


# def parse_pnp_data_multichart(host, service, start = '-1h', interval = '60'):
#     datapath = path.join(PERF_PATH, host)
#     xml_path = path.join(datapath, '%s.xml' % service)
#     rrd_path = path.join(datapath, '%s.rrd' % service)

#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     labels = [s.find('LABEL').text for s in root.findall('DATASOURCE')]
#     units = [s.find('UNIT').text for s in root.findall('DATASOURCE')]

#     rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE',
#         '--start', start, '-r', interval)
#     start, end, resolution = rrd_info[0]
#     rrd_rows = rrd_info[2]
#     data = {}
#     multi_chart = {}
#     #return units
#     index=0
#     for label_index, label in enumerate(labels): # we want a separate graph for every label
#         timestamp = start
#         if units[index]=="%%":
#             units[index]='%'
#         label_unit = labels[index]+' ['+units[index]+']'
#         result = []
#         for row in rrd_rows:
#             x = timestamp
#             y = row[label_index]
#             # if y is None: y = float('nan')
#             result.append({'timestamp': str(datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M')) , 'y': y})
#             timestamp+= resolution
#         elements_to_avg = len(result) / 120 # ex. if there are 120 elements, average every 2
#         index=index +1
#         data[label_unit] = result
#     data = [
#         {
#             "host_name" : x,
#             "zharts" : data[x],
#         }
#     for x in data]
#     return data

# def parse_multichart(host, service, start = '-1h', interval = '60'):
#     return parse_pnp_data_multichart(service, host, start, interval)