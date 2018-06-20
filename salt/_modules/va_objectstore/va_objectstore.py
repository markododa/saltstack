#!/usr/bin/python
from va_utils import check_functionality as panel_check_functionality
import salt, subprocess
import json, re

def get_config():
    data = json.load(open('/root/.minio/config.json'))
    return data

def get_auth():
    return get_config()['credential']

def panel_config():
    res = [{'key' : 'Access Key', 'value'  : get_config()['credential']['accessKey']}]
    res += [{'key' : 'Secret Key', 'value'  : get_config()['credential']['secretKey']}]
    res += [{'key' : 'Web access', 'value'  : "http://IP_ADDRESS:9000/minio/"}]
    return res

def panel_statistics():
    #diskusage =salt_dict['disk.usage']()[salt_dict['cmd.run']('findmnt --target /var/www/owncloud/ -o TARGET').split()[1]]
    diskusage = __salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /opt/minio/data/ -o TARGET').split()[1]]
    statistics = [{'key' : 'Storage partition used size (MB)', 'value': int(diskusage['used'])/1024},
                    {'key' : 'Storage partition free space (MB)', 'value': int(diskusage['available'])/1024},
                    {'key' : 'Storage partition mount point', 'value': diskusage['filesystem']}
                ]
    return statistics

def panel_list_buckets(path='/opt/minio/data/'):
    command = ['du', path, '-d1', '-b', '-m', '--exclude=.minio.sys'] 
    result = subprocess.check_output(command).split('\n')
    result = [re.sub(r'\s+', ' ', x).split(' ') for x in result if x]
    result = [{'path': path+x[1].split('/')[-1], 'size' : int(x[0]), 'bucket' : x[1].split('/')[-1]} for x in result if x[1].split('/')[-1] ]
    result = sorted(result, key = lambda x: x['bucket'], reverse = False)
    return result