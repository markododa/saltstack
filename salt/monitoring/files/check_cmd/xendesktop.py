#!/usr/bin/env python3
import json
from datetime import datetime as datetime
from datetime import timedelta as timedelta
import sys
import requests.auth
from requests_ntlm import HttpNtlmAuth

if (len(sys.argv) != 8):
    print("Usage: xendesktop.py username password path warning critical api_file minutes")
    quit()

username = sys.argv[1]
password = sys.argv[2]
path = sys.argv[3]
warning = int(sys.argv[4])
critical = int(sys.argv[5])
api_file = sys.argv[6]
minutes_diff = int(sys.argv[7])

def read_file(path,api_file):
    return json.load(open(api_file+'.json'))['value']

def read_api(path,api_file,username,password):
    URL = "http://" + path + "/Citrix/Monitor/OData/v2/Data/" + api_file + '?$format=json'
    session = requests.session()
    session.auth = HttpNtlmAuth(username,password)
    data = session.get(URL)._content
#    print(data)
    return json.loads(data.decode('utf-8'))['value']

def filter_by_date(json_data,date_key,minutes_diff):
    if minutes_diff == 0:
        return json_data
    filtered_json_data=[]
    for i in json_data:
        datestring = i[date_key].split('.')[0]
        timestamp = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')
        if ((datetime.now() - timedelta(minutes=minutes_diff)) < timestamp):
            filtered_json_data.append(i)
    return filtered_json_data


def monitoring_logic(count,warning,critical,text,perfdata):
    if int(count) < warning:
        print("OK: "+text+str(count)+perfdata)
        return 0
    elif int(count) > critical:
        print("CRITICAL: "+text+str(count)+perfdata)
        return 2
    elif int(count) > warning:
        print("WARNING: "+text+str(count)+perfdata)
        return 1
    else:
        pass

class FailureLogSummaries():
    def get(json_data,minutes_diff,warning,critical):
        count = 0
        for i in json_data:
         count+=i['FailureCount']
        return monitoring_logic(count,warning,critical,'Total Failure Count is ', "| failure_count="+str(count))
    def date_key():
        return 'CreatedDate'

class ConnectionFailureLogs():
    def get(json_data,minutes_diff,warning,critical):
        count = 0
        for i in json_data:
            count+=1
        return monitoring_logic(count,warning,critical,'Connection Failure Count is ', "| failure_count="+str(count))
    def date_key():
        return 'CreatedDate'

class MachineFailureLogs():
    def get(json_data,minutes_diff,warning,critical):
        count = 0
        for i in json_data:
            count+=1
        return monitoring_logic(count,warning,critical,'Machine Failure Count is ', "| failure_count="+str(count))
    def date_key():
        return 'CreatedDate'

class Machines():
    def get(json_data,minutes_diff,warning,critical):
        CurrentPowerStateCount = {}
        count=0
        for i in json_data:
            try:
                CurrentPowerStateCount[i['CurrentPowerState']]['count'] += 1
                CurrentPowerStateCount[i['CurrentPowerState']]['machines'] += [i['Name']]
            except:
                CurrentPowerStateCount[i['CurrentPowerState']] = {'count': 1, 'machines': [i['Name']]}
        #return json.dumps(CurrentPowerStateCount)
        for i in CurrentPowerStateCount:
            count+= CurrentPowerStateCount[i]['count']
            print('There are '+str(CurrentPowerStateCount[i]['count'])+' machines of type '+str(i))
        #    for machine in CurrentPowerStateCount[i]['machines']:
        #        print(machine)
        #return monitoring_logic(count,warning,critical,'Machine PowerStateCount is ', "| failure_count="+str(count))
        return 0
    def date_key():
        return 'CreatedDate'

def do_it(path, api_file, username, password, minutes_diff,warning,critical):
    custom_f = globals()[api_file]
#    json_data = read_file(path, api_file)
    json_data = read_api(path, api_file, username, password)
    json_data = filter_by_date(json_data,custom_f.date_key(),minutes_diff) 
    return custom_f.get(json_data,minutes_diff,warning,critical)


do_it(path=path, api_file=api_file,minutes_diff=minutes_diff, warning=warning,critical=critical, username=username,password=password)
