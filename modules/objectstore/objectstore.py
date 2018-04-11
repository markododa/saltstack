#!/usr/bin/python
import salt
import json

def get_config():
    data = json.load(open('/root/.minio/config.json'))
    return data

def get_auth():
    return get_config()['credential']

def panel_config():
    res = [{'key' : 'Access Key', 'value'  : get_config()['credential']['accessKey']}]
    res += [{'key' : 'Secret Key', 'value'  : get_config()['credential']['secretKey']}]
    return res