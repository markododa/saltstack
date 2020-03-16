#!/usr/bin/env python
import xml.etree.ElementTree as ET
import datetime, time
from os import path

PERF_PATH = '/var/lib/pnp4nagios/perfdata'

def parse_pnp_data(host, service, start = '-1h', interval = '60'):
    datapath = path.join(PERF_PATH, host)
    xml_path = path.join(datapath, '%s.xml' % service)
    rrd_path = path.join(datapath, '%s.rrd' % service)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    labels = [s.find('LABEL').text for s in root.findall('DATASOURCE')]
    units = [s.find('UNIT').text for s in root.findall('DATASOURCE')]

    rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE',
        '--start', start, '-r', interval)
    start, end, resolution = rrd_info[0]
    rrd_rows = rrd_info[2]
    data = {}
    #return units
    index=0
    for label_index, label in enumerate(labels): # we want a separate graph for every label
        timestamp = start
        if units[index]:
            units[index].replace('%%','%')
            label_unit = labels[index]+' ('+units[index]+')'
        else:
            label_unit = labels[index]
        result = []
        for row in rrd_rows:
            x = timestamp
            y = row[label_index]
            # if y is None: y = float('nan')
            result.append({'x': x, 'y': y, 'label_unit':label_unit})
            timestamp+= resolution
        elements_to_avg = len(result) / 120 # ex. if there are 120 elements, average every 2
        #new_result = [{'y': sum([el['y'] for el in grouped]) / elements_to_avg, 'x': grouped[0]['x']} \
                     #for grouped in zip(*[iter(result)] * elements_to_avg)]
        data[label_unit] = result
        index=index +1
    return data

def parse(host, service, start = '-1h', interval = '60'):
    return parse_pnp_data(host, service, start, interval)

def parse_get_table(host, service, start = '-1h', interval = '60'):
    pnp_data = parse_pnp_data(host, service, start, interval)
    pnp_data = [{'ts' : i['x'], key : i['y']} for key in pnp_data for i in pnp_data[key]]
    return pnp_data


def parse_pnp_data_multichart(host, service, start = '-1h', interval = '60'):
    datapath = path.join(PERF_PATH, host)
    xml_path = path.join(datapath, '%s.xml' % service)
    rrd_path = path.join(datapath, '%s.rrd' % service)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    labels = [s.find('LABEL').text for s in root.findall('DATASOURCE')]
    units = [s.find('UNIT').text for s in root.findall('DATASOURCE')]

    rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE',
        '--start', start, '-r', interval)
    start, end, resolution = rrd_info[0]
    rrd_rows = rrd_info[2]
    data = {}
    multi_chart = {}
    #return units
    index=0
    for label_index, label in enumerate(labels): # we want a separate graph for every label
        timestamp = start
        if units[index]=="%%":
            units[index]='%'
        label_unit = labels[index]+' ['+units[index]+']'
        result = []
        for row in rrd_rows:
            x = timestamp
            y = row[label_index]
            # if y is None: y = float('nan')
            result.append({'timestamp': str(datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M')) , 'y': y})
            timestamp+= resolution
        elements_to_avg = len(result) / 120 # ex. if there are 120 elements, average every 2
        index=index +1
        data[label_unit] = result
    data = [
        {
            "host_name" : x,
            "zharts" : data[x],
        } 
    for x in data]
    return data

def parse_multichart(host, service, start = '-1h', interval = '60'):
    return parse_pnp_data_multichart(service, host, start, interval)
