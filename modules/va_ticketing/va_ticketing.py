import subprocess
import requests
import json
import re
import time, datetime
import salt

from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_ticketing_panels import panels

def get_panel(panel_name, provider='', service=''):
    users_panel = panels[panel_name]
    if panel_name == 'ticketing.functionality':
        data = minions_functionality()
        users_panel['tbl_source'] = data
        return users_panel
    elif panel_name == 'ticketing.keys':
        data = salt_keys()
        users_panel['tbl_source'] = {"table":data}
        return users_panel
    elif panel_name == 'ticketing.details':
        data = icinga2_singlehost(provider)
        for host in data: 
            for service in host['services']:
                service['host_name'] = host['host_name'] 
        data1 = {x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data1
        return users_panel

