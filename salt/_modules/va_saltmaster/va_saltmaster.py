import subprocess
import requests
import json
import re
import time, datetime
import salt

from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_saltmaster_panels import panels


integrations_text = {
    'monitoring' : 'This will install and configure the NRPE agent on the Linux target. The agent will do local tests and return the results to the Monitoring App',
    'directory'  : 'Does not provide out-of-the-box integration. A new user will be created in the Directory and all the details will be written in /root/integration_directory.txt on the target. Adjust the grouo membership of the user to control the permissions.',
    'backup'     : 'SSH key will be uploaded to the target so that the user named backuppc will have access. Rsync will also be installed. Default backup paths will be imported. Manually review the Backup App panels later for adjusting other settings.',
    'backup4'     : 'SSH key will be uploaded to the target so that the user named backuppc will have access. Rsync will also be installed. Default backup paths will be imported. Manually review the Backup4 App panels later for adjusting other settings.',
    'email'      : 'Does not provide out-of-the-box integration. Mail server details will be written in /root/integration_email.txt. Directory integration might be required for authentication too.'
}

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

def get_minion_grains(minion):
    grains = __salt__['cmd.run']('salt '+minion+' grains.items --output=json',runas='root', cwd = '/',python_shell=True)
    grains = grains.replace('\n','').replace('}{',',').replace('Minion did not return. ','')
    grains = json.loads(grains)
    return grains

def panel_minion_grains(minion):
    grains=get_minion_grains(minion)
    keys=[]
    # for key in grains:
    keys.append({"item":"Hypervisor", "value" : grains[minion]["virtual"]})
    keys.append({"item":"Cores", "value" : grains[minion]["num_cpus"]})
    keys.append({"item":"Memory (MB)", "value" : grains[minion]["mem_total"]})
    keys.append({"item":"Swap (MB)", "value" : grains[minion]["swap_total"]})


    lista=grains[minion]["disks"]
    if not lista:
        raise Exception("Error")
    else:
        result = []
        for item in lista:
            if not "loop" in item:
                result.append(item)

    keys.append({"item":"Disks", "value" : result})


    lista=grains[minion]["ipv4"]
    if not lista:
        raise Exception("Error")
    else:
        result = []
        for item in lista:
            if item != '127.0.0.1':
                result.append(item)

    keys.append({"item":"IPs", "value" : result})

    return keys


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


def list_minion_ssh_keys(minion):
    out = __salt__['cmd.run']('salt '+minion+' ssh.auth_keys root -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    # return out
    keys=[]
    for key in out[minion]:
        keys.append({"minion":minion, "comment": out[minion][key]["comment"], "enc": out[minion][key]["enc"], "fingerprint": out[minion][key]["fingerprint"].replace(':', ''), "key": key, "key_short": key[:10]+'...'+key[(len(key)-20):]})
    return keys

def list_minions_ssh_keys():
    # out = __salt__['cmd.run']('salt-run manage.status -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
    # out = json.loads(out)
    # out=[]
    out={'va-master'}
    all_keys=[]
    # return out
    for minion in out:
        keys=list_minion_ssh_keys(minion)
        # keys=[{"aaa":"sss"}]
        for key in keys:
            key['id']='text'
            all_keys.append(key)
        # minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":grains[minion]["role"]})
    return all_keys

def list_minions():
    out = __salt__['cmd.run']('salt-run manage.status -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
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


def translate_pillars(pillar):
    known_pillars = {'query_user' : 'LDAP Query user', 'domain' : 'Company Domain', 'query_password' : 'LDAP Query user password', 'shortdomain' : 'Company domain (short version)', 'proxy_ip' : 'IP address for Proxy app', 'admin_password' : 'Administrator password', 'timezone' : 'Default time zone', 'redmine_password' : 'Redmine SQL password', 'openstackhost' : 'OpenStack host', 'openstackpass' : 'OpenStack Password', 'openstacktenant' : 'OpenStack tenant', 'openstackuser' : 'OpenStack user', 'ssh-key' : 'OpenStack SSH key', 'net-id' : 'OpenStack network ID', 'endpointurl' : 'OpenStack endpoint URL'}
    if pillar in known_pillars:
        pillar=known_pillars[pillar]
    else:
        pillar="_Undefined_"
    return pillar


def list_pillars():
    out = __salt__['cmd.run']('salt va-master pillar.items --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    pillars=[]
    for pillar in out["va-master"]:
        if type(out["va-master"][pillar]) in [str, unicode]:
            pillars.append({"pillar":pillar, "human_name":translate_pillars(pillar), "value": out["va-master"][pillar]})
    pillars = sorted(pillars, key = lambda x: x['human_name'], reverse = False)
    return pillars



def list_minions_details():
    minions=[]
    grains=get_all_grains()
    for minion in grains:
        if type(grains[minion]) in [str, unicode]:
            minions.append({"minion":minion, "state": "Critical", "status": "Down", "saltversion":"", "os":"", "role":grains[minion]})
        else:
            minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":grains[minion]["role"]})
    return minions

def list_minions_integrations():
    out = __salt__['cmd.run']('salt-run manage.up --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    grains=get_all_grains()
    for minion in out:
        minions.append({"minion":minion, "integrations":integrations_text.get(grains[minion]["role"],"- Does not provide integration -"), "role":grains[minion]["role"]})
    return minions


def list_minions_down():
    out = __salt__['cmd.run']('salt-run manage.down --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    for minion in out:
        minions.append({"minion":minion})
    return minions
