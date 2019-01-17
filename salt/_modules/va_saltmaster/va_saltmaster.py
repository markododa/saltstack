import subprocess
import requests
import json
import re
import time, datetime
import salt

from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_saltmaster_panels import panels


integrations_result = {
    'monitoring-any' : 'This will install and configure the NRPE agent on the Linux target. The agent will do local tests and return the results to the Monitoring App',
    'directory-any'  : 'Does not provide out-of-the-box integration. A new user will be created in the Directory and all the details will be written in /root/integration_directory.txt on the target. Adjust the group membership of the user to control the permissions.',
    'directory-cloudshare'  : 'A new user will be created in the Directory and LDAB as user backend will be configured on Cloudshare so all daomin users can use same credentails on this app too.',
    'directory-monitoring'  : 'Creates a new administrator user in Directory. The details will be written /etc/icinga2/conf.d/cred_win_domain.txt and will be used to remote monitor Windows targets.',
    'directory-email'  : 'Configure LDAP as user backend, special query user will be used to check the passwords. All Directory user will have own mailboxes immidietly.',
    'directory-directory'  : "- No integration possible -",
    'directory-fileshare'  : "This will join the fileshare app to the Domain Controller",
    'backup-any'     : 'SSH key will be uploaded to the target so that the user named backuppc will have access. Rsync will also be installed. Default backup paths will be imported. Manually review the Backup App panels later for adjusting other settings.',
    'backup4-any'     : 'SSH key will be uploaded to the target so that the user named backuppc will have access. Rsync will also be installed. Default backup paths will be imported. Manually review the Backup4 App panels later for adjusting other settings.',
    'email-any'      : 'Does not provide out-of-the-box integration. Mail server details will be written in /root/integration_email.txt.',
    'email-monitoring'      : 'Will adjust the config file /etc/ssmtp/ssmtp.conf so email notifications will be possible. Be sure to manually input user/password data later'
}

integrations_text = {
    'monitoring' : 'Provides monitoring of critical components on the target server',
    'directory'  : 'Porvides centralized user and password management.',
    'backup'     : 'Provides file level backup using SSH or SMB protocol from a remote server.',
    'backup4'     : 'Provides file level backup using SSH or SMB protocol from a remote server.',
    'email'      : 'Provides email sending capabilities from specific apps.'
}

#This should be called for parsing output from salt and targeting more then one minion as salt produce broken JSON
def fix_salt_json(json):
    out=json.replace('\n', '')
    out=out.replace('}{',' ,')
    out=out.replace('ERROR: Minions returned with non-zero exit code','')
    out=out.replace('Minion did not return. ','')
    return out


#It would be better to test for non zero exit code when single minion is called
def test_salt_out(out):
    if out.find("ERROR: Minions returned with non-zero exit code")>-1:
        return False
    elif out.find("The module cannot be loaded")>-1:
        return False
    else:
        return True


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


def minions_functionality():
    out = __salt__['cmd.run']('salt "*" va_utils.check_functionality --output=json',runas='root', cwd = '/',python_shell=True)
    out=fix_salt_json(out)
    out = json.loads(out)
    #return out
    for result in out:
        if type(out[result]) in [str, unicode]:
            out[result] = [{"output":out[result], "state": "Unknown"}]
    return out


def get_minion_os(minion):
    role = __salt__['cmd.run']('salt "'+minion+'" grains.get osfinger --output=json',runas='root', cwd = '/',python_shell=True)
    role = json.loads(role)
    role= role[minion]
    if role:
        return role
    else:
        return "-"


def get_all_grains():
    grains = __salt__['cmd.run']('salt "*" grains.items -t 1 --output=json',runas='root', cwd = '/',python_shell=True)
    grains=fix_salt_json(grains)
    grains = json.loads(grains)
    return grains


def get_minion_grains(minion):
    grains = __salt__['cmd.run']('salt "'+minion+'" grains.items --output=json',runas='root', cwd = '/',python_shell=True)
    grains=fix_salt_json(grains)
    grains = json.loads(grains)
    return grains


def panel_minion_grains(minion):
    grains=get_minion_grains(minion)
    keys=[]
    # for key in grains:
    keys.append({"item":"Hypervisor", "value" : grains[minion].get("virtual") or "-"})
    keys.append({"item":"Cores", "value" : grains[minion].get("num_cpus") or "-"})
    keys.append({"item":"Memory (MB)", "value" : grains[minion].get("mem_total") or "-"})
    keys.append({"item":"Swap (MB)", "value" : grains[minion].get("swap_total") or "-"})

    lista=grains[minion]["disks"]

    if not lista:
        keys.append({"item":"Disks", "value" : "-"})
        # raise Exception("Error")
    else:
        result = []
        for item in lista:
            if not "loop" in item:
                result.append(item)
        keys.append({"item":"Disks", "value" : result})

    lista=grains[minion]["ipv4"]
    if not lista:
        # raise Exception("Error")
        keys.append({"item":"IPs", "value" : "-"})
    else:
        result = []
        for item in lista:
            if item != '127.0.0.1':
                result.append(item)
        keys.append({"item":"IPs", "value" : result})

    return keys


def minion_key_delete(minion):
    out = __salt__['cmd.run']('salt-key -y -d "'+minion+'"',runas='root', cwd = '/',python_shell=True)
    # return out


def minion_key_accept(minion):
    out = __salt__['cmd.run']('salt-key -y -a "'+minion + '" --include-rejected --include-denied',runas='root', cwd = '/',python_shell=True)
    # return out


def minion_key_reject(minion):
    out = __salt__['cmd.run']('salt-key -y -r "'+minion + '" --include-accepted --include-denied',runas='root', cwd = '/',python_shell=True)
    # return out


def salt_keys():
    out = __salt__['cmd.run']('salt-key --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    for minion in out['minions_rejected']:
        minions.append({"minion":minion, "state": "Critical", "status": "Rejected"})
    for minion in out['minions_denied']:
        minions.append({"minion":minion, "state": "Warning", "status": "Denied"})
    for minion in out['minions_pre']:
        minions.append({"minion":minion, "state": "Pending", "status": "Unaccepted"})
    for minion in out['minions']:
        minions.append({"minion":minion, "state": "OK", "status": "Accepted", "role": ""})
    return minions



def list_minion_upgrades(minion):
    out = __salt__['cmd.run']('salt "'+minion+'"  pkg.list_upgrades dist_upgrade=False -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    # return out
    keys=[]
    for key in out[minion]:
        keys.append({"package": key, "ver":out[minion][key]})
    return keys


def bulk_update_minions(bulk_update_command,distro):
    if distro:
        do_distro="True"
    else:
        do_distro="False"

    if bulk_update_command=='Check for updates':
        out = __salt__['cmd.run']('salt \*  pkg.list_upgrades dist_upgrade='+do_distro+' -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
    if bulk_update_command=='Upgrade all':
        out = __salt__['cmd.run']('salt \*  pkg.upgrade dist_upgrade='+do_distro+' -t 300 --output=json',runas='root', cwd = '/',python_shell=True)

    out=fix_salt_json(out)
    return out


	# "va-master": {},
	# "directory": {},
	# "directory2": {
	# 	"winbind": "2:4.7.6+dfsg~ubuntu-0ubuntu2.5",
	# 	"unattended-upgrades": "1.1ubuntu1.18.04.8",
	# 	"libnss-winbind": "2:4.7.6+dfsg~ubuntu-0ubuntu2.5",
	# 	"libpam-winbind": "2:4.7.6+dfsg~ubuntu-0ubuntu2.5"
	# },
	# "backup4": {
	# 	"tzdata": "2018i-0ubuntu0.18.04"
	# },
	# "files": "[Not connected]"

    out = json.loads(out)
    minions = 0
    items = 0
    for minion in out:
        if type(out[minion]) not in [str, unicode]:
            minions=minions+1
            for keys in out[minion]:
                if type(out[minion][keys]) not in [str, unicode]:
                    items=items+len(out[minion][keys])
    total_items = str(items)
    total_minions = str(minions)
    return bulk_update_command


def minion_upgrade(minion,package):
    out = __salt__['cmd.run']('salt "'+minion+'"  pkg.install ' + package +' -t 100 --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    packages = str(len(out[minion]))
    return "Upgraded "+packages+" package(s)"
    #return len(out[minion])

    # In case of error:
    # va-master:
    # ERROR: Problem encountered installing package(s). Additional info follows:

    # changes:
    #     ----------
    # errors:
    #     - Running scope as unit: run-r9ef9317441ac49d3bae844638b61e554.scope
    #       E: Unable to locate package patch12


def minion_upgrade_all(minion):
    out = __salt__['cmd.run']('salt "'+minion+'"  pkg.upgrade --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    packages = str(len(out[minion]))
    return "Upgraded "+packages+" package(s)"


def salt_sync_all():
    out = __salt__['cmd.run']('salt \* saltutil.sync_all -t 1 --output=json',runas='root', cwd = '/',python_shell=True)
    out=fix_salt_json(out)
    # return out
    out = json.loads(out)
    minions = 0
    items = 0
    for minion in out:
        if type(out[minion]) not in [str, unicode]:
            minions=minions+1
            for keys in out[minion]:
                if type(out[minion][keys]) not in [str, unicode]:
                    for key in out[minion][keys]:
                        items=items+len(out[minion][keys])
    total_items = str(items)
    total_minions = str(minions)
    return "Synced "+total_minions+" minions(s) and "+ total_items+" item(s)"


def list_store_ssh_keys():
    minion='va-master'
    out = __salt__['cmd.run']('salt "va-master" ssh.auth_keys user=root config="/root/ssh-store.txt" -t 30 --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    # return out
    keys=[]
    for key in out[minion]:
        keys.append({"minion":"dd", "comment": out[minion][key]["comment"], "enc": out[minion][key]["enc"], "fingerprint": out[minion][key]["fingerprint"].replace(':', ''), "key": key, "key_short": key[:10]+'...'+key[(len(key)-20):]})
    return keys


def list_minion_ssh_keys(minion):
    out = __salt__['cmd.run']('salt "'+minion+'" ssh.auth_keys user=root --output=json',runas='root', cwd = '/',python_shell=True)
    # return test_salt_out(out)
    if test_salt_out(out):
        out = json.loads(out)
    else:
        return [] #"Error"
    # return out
    keys=[]
    for key in out[minion]:
        keys.append({"minion":minion, "comment": out[minion][key]["comment"], "enc": out[minion][key]["enc"], "fingerprint": out[minion][key]["fingerprint"].replace(':', ''), "key": key, "key_short": key[:10]+'...'+key[(len(key)-20):]})
    return keys


def list_minions_ssh_keys():
    all_keys=[]
    keys=list_minion_ssh_keys('va-master')
    for key in keys:
        key['id']='text'
        all_keys.append(key)
    return all_keys


def key_to_store(comment,enc,key):
    return add_ssh_key_store(comment,enc,key)


def download_pubkey(comment,enc,key):
    #Should output a file TODO
    return str(comment)+" " +str(enc)+" "+str(key)


def add_ssh_key_store(comment,enc,key):
    out = __salt__['cmd.run']('salt "va-master" ssh.set_auth_key root "'+str(key)+'" enc="'+str(enc)+'" comment="'+str(comment)+'" config="/root/ssh-store.txt" --output=json',runas='root', cwd = '/',python_shell=True)
    if test_salt_out(out):
        out = json.loads(out)
        return out["va-master"]
    else:
        return "Error while executing the command" #"Error"


def upload_ssh_key_minion(comment,enc,key,minion):
    out = __salt__['cmd.run']('salt "'+minion+'" ssh.set_auth_key root "'+str(key)+'" enc="'+str(enc)+'" comment="'+str(comment)+'" --output=json',runas='root', cwd = '/',python_shell=True)
    if test_salt_out(out):
        out = json.loads(out)
        return out[minion]
    else:
        return "Error while executing the command" #"Error"


def ssh_key_delete_store(comment,enc,key):
    out = __salt__['cmd.run']('salt "va-master" ssh.rm_auth_key root "'+str(key)+'" config="/root/ssh-store.txt" --output=json',runas='root', cwd = '/',python_shell=True)
    if test_salt_out(out):
        out = json.loads(out)
        return out["va-master"]
    else:
        return "Error while executing the command" #"Error"


def remove_ssh_key_minion(junk,comment,enc,key,minion):
    out = __salt__['cmd.run']('salt "'+minion+'" ssh.rm_auth_key root "'+str(key)+'" --output=json',runas='root', cwd = '/',python_shell=True)
    if test_salt_out(out):
        out = json.loads(out)
        return out[minion]
    else:
        return "Error while executing the command" #"Error"


def list_minions():
    out = __salt__['cmd.run']('salt-run manage.status -t 3 --output=json',runas='root', cwd = '/',python_shell=True)
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
        minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":(grains[minion].get("role") or "-")})
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
            minions.append({"minion":minion, "state": "OK", "status": "Up", "saltversion":grains[minion]["saltversion"], "os":grains[minion]["osfinger"], "role":(grains[minion].get("role") or "-")})
    return minions


def list_minions_integrations():
    out = __salt__['cmd.run']('salt-run manage.up --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    grains=get_all_grains()
    for minion in out:
        minions.append({"minion":minion, "integrations":integrations_text.get(grains[minion].get("role") or "-","- Does not provide integration -"), "role":(grains[minion].get("role") or "-")})
    return minions

def apply_minions_integrations(minion, role):
    #return minion+" "+role
    out = __salt__['cmd.run']('salt-run manage.up --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    targets=[]
    grains=get_all_grains()
    for target in out:
        if target != minion:
            target_role=grains[target].get("role") or "-"
            lookup=role+"-"+target_role
            targets.append({"from":minion+" ("+role+")","to":target+" ("+target_role+")","minion":minion,"role":role,"target":target, "lookfor":lookup, "integrations":integrations_result.get(lookup,integrations_result.get(role+"-any","- No integration possible -")), "target_role":target_role})
    return targets


def apply_integration_state(junk, minion, role, lookfor, target, lookup):
    return "Pure Magic"



def list_minions_down():
    out = __salt__['cmd.run']('salt-run manage.down --output=json',runas='root', cwd = '/',python_shell=True)
    out = json.loads(out)
    minions=[]
    for minion in out:
        minions.append({"minion":minion})
    return minions
