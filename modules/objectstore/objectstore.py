#!/usr/bin/python
import salt
import json

def get_config():
    data = json.load(open('/root/.minio/config.json'))
    return data

def get_auth():
    return get_config()['credential']
