import subprocess
import requests
import json
import re
import time, datetime
import salt

from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_saltmaster_panels import panels

def get_panel(panel_name, provider='', service=''):
    users_panel = panels[panel_name]
    if panel_name == 'saltmaster.functionality':
        data = minions_functionality()
        users_panel['tbl_source'] = data
        return users_panel
    elif panel_name == 'saltmaster.keys':
        data = salt_keys()
        users_panel['tbl_source'] = {"table":data}
        return users_panel
    # elif panel_name == 'saltmaster.minions':
    #     data = list_minions()
    #     users_panel['tbl_source'] = {"table":data}
    #     return users_panel
    elif panel_name == 'saltmaster.details':
        data = icinga2_singlehost(provider)
        for host in data: 
            for service in host['services']:
                service['host_name'] = host['host_name'] 
        data1 = {x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data1
        return users_panel


def minions_functionality():
    out = __salt__['cmd.run']('salt "*" va_utils.check_functionality --output=json',runas='root', cwd = '/',python_shell=True)
    out=out.replace('\n', '')
    out=out.replace('}{',' ,')
    # return '{'+out+'}'
    out = json.loads(out)
    # return out
    for result in out:
        if type(out[result]) in [str, unicode]:
            out[result] = [{"output":out[result], "state": "Unknown"}]
    return out

# def get_minion_role(minion):
#     role = __salt__['cmd.run']('salt '+minion+' grains.get role --output=json',runas='root', cwd = '/',python_shell=True)
#     role = json.loads(role)
#     return role

def get_minion_os(minion):
    role = __salt__['cmd.run']('salt '+minion+' grains.get osfinger --output=json',runas='root', cwd = '/',python_shell=True)
    role = json.loads(role)
    role= role[minion]
    if role:
        return role
    else:
        return "-"

def get_all_grains():
    grains = __salt__['cmd.run']('salt "*" grains.items --output=json',runas='root', cwd = '/',python_shell=True)
    grains = grains.replace('\n','').replace('}{',',').replace('Minion did not return. ','')
    grains = json.loads(grains)
    return grains


def minion_key_delete(minion):
    out = __salt__['cmd.run']('salt-key -y -d '+minion,runas='root', cwd = '/',python_shell=True)
    # return out

def minion_key_accept(minion):
    out = __salt__['cmd.run']('salt-key -y -a '+minion + ' --include-rejected --include-denied',runas='root', cwd = '/',python_shell=True)
    # return out

def minion_key_reject(minion):
    out = __salt__['cmd.run']('salt-key -y -r '+minion + ' --include-accepted --include-denied',runas='root', cwd = '/',python_shell=True)
    # return out

def salt_keys():
    out = __salt__['cmd.run']('salt-key --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    # roles = __salt__['cmd.run']('salt "*" grains.get role --output=json',runas='root', cwd = '/',python_shell=True)
    # # NOT really a JSON output, need fixing
    # roles = roles.replace('\n','').replace('}{',',').replace('Minion did not return. ','')
    # roles = json.loads(roles)

    for minion in out['minions_rejected']:
        minions.append({"minion":minion, "state": "Critical", "status": "Rejected"})
    for minion in out['minions_denied']:
        minions.append({"minion":minion, "state": "Warning", "status": "Denied"})
    for minion in out['minions_pre']:
        minions.append({"minion":minion, "state": "Pending", "status": "Unaccepted"})
    for minion in out['minions']:
        minions.append({"minion":minion, "state": "OK", "status": "Accepted", "role": ""})
        # minions.append({"minion":minion, "state": "OK", "status": "Accepted", "role": roles[minion]})
    return minions


def list_minions():
    out = __salt__['cmd.run']('salt-run manage.status --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    for minion in out['down']:
        minions.append({"minion":minion, "state": "Critical", "status": "Down"})
    for minion in out['up']:
        minions.append({"minion":minion, "state": "OK", "status": "Up"})
    return minions

def list_minions_up():
    out = __salt__['cmd.run']('salt-run manage.up --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    grains=get_all_grains()
    for minion in out:
        minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":grains[minion]["role"]})
    return minions

def list_minions_details():
    minions=[]
    grains=get_all_grains()
    for minion in grains:
        if type(grains[minion]) in [str, unicode]:
            minions.append({"minion":minion, "state": "Critical", "status": "Down", "saltversion":"", "os":"", "role":grains[minion]})
        else:
            minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":grains[minion]["role"]})
    return minions


def list_minions_down():
    out = __salt__['cmd.run']('salt-run manage.down --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    for minion in out:
        minions.append({"minion":minion})
    return minions