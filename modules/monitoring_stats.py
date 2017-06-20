#!/usr/bin/env python
import xml.etree.ElementTree as ET
import rrdtool
from os import path

PERF_PATH = '/var/lib/pnp4nagios/perfdata'

def parse(host, service, start = '-1h', interval = '60'):
   datapath = path.join(PERF_PATH, host)
   xml_path = path.join(datapath, '%s.xml' % service)
   rrd_path = path.join(datapath, '%s.rrd' % service)

   tree = ET.parse(xml_path)
   root = tree.getroot()
   labels = [s.find('LABEL').text for s in root.findall('DATASOURCE')]

   rrd_info = rrdtool.fetch(rrd_path, 'AVERAGE',
       '--start', start, '-r', interval)
   start, end, resolution = rrd_info[0]
   rrd_rows = rrd_info[2]
   data = {}
   for label_index, label in enumerate(labels): # we want a separate graph for every label
       timestamp = start
       result = []
       for row in rrd_rows:
           x = timestamp
           y = row[label_index]
           # if y is None: y = float('nan')
           result.append({'x': x, 'y': y})
           timestamp+= resolution
       elements_to_avg = len(result) / 120 # ex. if there are 120 elements, average every 2
       #new_result = [{'y': sum([el['y'] for el in grouped]) / elements_to_avg, 'x': grouped[0]['x']} \
                     #for grouped in zip(*[iter(result)] * elements_to_avg)]
       data[label] = result
   return data
