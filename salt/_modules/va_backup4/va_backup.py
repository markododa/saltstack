import va_utils, salt, os.path, os, json, datetime, time, re, subprocess, fnmatch

from va_utils import check_functionality as panel_check_functionality
from va_backup_panels import panels
from pool_stats import parse_pool_data
# from pool_stats import parse_multichart

backuppc_dir = '/etc/backuppc/'
backuppc_pc_dir = '/etc/backuppc/pc'
backuppc_hosts = '/etc/backuppc/hosts'
sshcmd='ssh -oStrictHostKeyChecking=no root@'
rm_key='ssh-keygen -f "/var/lib/backuppc/.ssh/known_hosts" -R '

#Used when converting hash to json - replaces all instances of the first char with the second one.
#Backslashes are a nightmare; json likes to have double backslashes. So we take any already double backslashes and reduce them by half, and then double all backslashes.
hash_to_json_characters_map = [('undef', 'null'),('(', '{'), (')', '}'), ('\\\\', '\\'), ('\\', '\\\\'), ('\n', ''), ('=>', ':'), ('\'', '"'), (';', ','), ('=', ':')]
json_to_hash_characters_map = [(':', '=>'), (':','='), ('"', '\'')]


#duplicate from cloudshare
def bytes_to_readable(num, suffix='B'):
    """Converts bytes integer to human readable"""

    num = int(num)
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

default_paths = {
    'monitoring' : ['/etc/icinga2', '/root/.va/backup/', '/etc/ssmtp/', '/usr/lib/nagios/plugins/',  '/var/lib/pnp4nagios/perfdata/', '/etc/nagios/nrpe.d/'],
    'directory'  : ['/etc/samba/', '/var/lib/samba/', '/etc/nagios/nrpe.d/'],
    'backup'     : ['/etc/backuppc/', '/etc/nagios/nrpe.d/'],
    'fileshare'  : ['/home/', '/etc/samba/', '/etc/nagios/nrpe.d/'],
    'email'      : ['/etc/postfix/', '/root/.va/backup/', '/var/vmail/', '/etc/nagios/nrpe.d/'],
    'cloudshare' : ['/root/.va/backup/', '/var/www/owncloud/', '/etc/nagios/nrpe.d/'],
    'owncloud'   : ['/root/.va/backup/', '/var/www/owncloud/', '/etc/nagios/nrpe.d/'],
    'proxy'      : ['/etc/lighttpd/', '/etc/squid/', '/var/www/html/', '/etc/e2guardian/', '/usr/share/e2guardian/', '/etc/nagios/nrpe.d/'],
    'ticketing'  : ['/root/.va/backup/'],
    'objectstore': ['/opt/minio/data'],
    'va-master'  : ['/opt/va_master/', '/srv/', '/etc/openvpn/']
}

def host_file(hostname):
    filename = backuppc_pc_dir+'/'+hostname+'.pl'
    return filename

def get_panel(panel_name, server_name = '', backupNum = -1):
    if panel_name == "backup.browse":
        host = server_name
        ppanel = panels[panel_name]
        hostnames = listHosts()
        host = hostnames[0] if host == '' else host
        if backupNum == -1:
            backupNum = last_backup(host)
        data = dir_structure1(host, backupNum)
        ppanel['form_source'] = {"dropdown": {}}
        ppanel["form_source"]["dropdown"]["values"] = hostnames
        ppanel["form_source"]["dropdown"]["select"] = host
        ppanel['tbl_source']['table'] = data
        ppanel['tbl_source']['path'] = [host, backupNum]
        return ppanel


def dir_structure1_old(host, *args):
    check = False
    if len(args) == 0:
        backupNum = last_backup(host)
        attrib = backup_attrib(host, backupNum)
        check = True
    else:
        backupNum = args[0]
        attrib = backup_attrib(host, *args)
        args = args[1:]
    data = dir_structure(host, backupNum)
    if data == "No files available.":
        return []
    for x in args:
        data = data[x]
    result = []
    for key,val in data.items():
        type = 'folder' if val is not None else 'file'
        time = '/'
        size = '...'
        if key in attrib:
            a = attrib[key]
            size, time = (a['size'], a['time'])
        if type == 'folder' or size != '...':
            if type == 'folder':
                sortkey = 'a'
            else:
                sortkey = 'z'
            result.append({'dir': key, 'type': type, 'size': size, 'time': time, 'sortkey': sortkey});
    if check:
        return {'val': backupNum, 'list': result}
    [d.update({'size' : ''}) for d in result if d['type'] == 'folder']
    result = sorted(result, key = lambda x: (x['sortkey'],x['dir'].lower()), reverse = False)
    return result


def dir_structure1(host, *args):
    check = False
    if len(args) == 0:
        backupNum = last_backup(host)
        attrib = backup_attrib(host, backupNum)
        check = True
    elif len(args) == 1:
        backupNum = args[0]
        attrib = backup_attrib(host, *args)
        args = args[1:]
        result = []
        shares =  get_folders_from_config(host)
        for share in shares:
            result.append({'hash':'','type':'folder',"permissions": '', 'unknown' :'','size': '','dir': share, 'time': '/'})
        return result
    else:
        backupNum = args[0]
        # attrib = backup_attrib(host, *args)
        args = args[1:]
        share = args[0]
        args = args[1:]
        path='/'.join([str(x) for x in args])
        path='/'+path
        pathlen=len(path)
        if path=='/':
            pathlen=0
        path='"'+path+'"'
        host ='"'+str(host)+'"'
        backupNum = '"'+str(backupNum)+'"'
        share = '"'+str(share)+'"'
        bash_cmd = ['/bin/su','-s', '/bin/sh', 'backuppc', '-c','/usr/local/backuppc/bin/BackupPC_ls -h ' + host + ' -n ' + backupNum + ' -s ' + share + ' ' + path]

        try:
            text = subprocess.check_output(bash_cmd)
            text = text.split('\n')
            text = text[1:]
            result =[]
            for line in text:
                part = line.split(' ')
                if len(part) > 6:
                # return part
                    perm = line[0:10]
                    unknown = line[11:20].strip()

                    timestamp = line[32:51]
                    filename = line.split('/')[2:]
                    filename= '/'.join(filename).rstrip()
                    filename=filename[pathlen:]

                    if line[0]=='d':
                        ftype='folder'
                        fhash=''
                        filename=filename[0:len(filename)-1]
                        sortkey='a'
                        size=''
                    else:
                        ftype='file'
                        filename=filename.split('(')
                        fhash=filename[len(filename)-1]
                        fhash=fhash[0:len(fhash)-1]
                        filename=filename[0:len(filename)-1]
                        filename= '('.join(filename).rstrip()
                        sortkey='z'
                        size = long(line[21:31].strip())

                    result.append({'sortkey':sortkey,"hash":fhash,'type':ftype,"permissions": perm, 'unknown' :unknown,'size': size,'dir': filename, 'time': timestamp, 'zzzz_all':path})

            result = sorted(result, key = lambda x: (x['sortkey'],x['dir'].lower()), reverse = False)
            return result
        except subprocess.CalledProcessError as e:
            return "No files available."



def get_path_from_backup_number(hostname, backupnumber):
    path = '/var/lib/backuppc/pc/'+hostname+'/'+str(backupnumber)
    return path

def last_backup(host):
    result = map(int, backupNumbers(host))
    backupNum = max(backupNumbers(host))
    return backupNum

def get_backup_pubkey():
    file_contents = ''
    with open('/var/lib/backuppc/.ssh/id_rsa.pub') as f:
        file_contents = f.read()
    return file_contents

def add_default_paths(hosts = []):
    for host in hosts:
        role= get_role(host)
        paths = default_paths.get(role,['/root/.va/backup'])

        for path in paths:
            result = add_folder(host, path)
    return True

def test_ip_ssh(ip_addr):
    try:
        cmd = ['nc', '-w','3','-z', ip_addr, '22']
        x=subprocess.call(cmd)
        if x:
            return False
        else:
            return True
    except:
        return False

def test_session_ssh(ip_addr, r_user='root', l_user=None):
    # return True
    try:
        if not l_user:
            cmd = ['ssh', '-q', r_user+'@'+ip_addr, ' exit']
        else:
            cmd = ['/bin/su','-s', '/bin/sh', l_user, '-c', 'ssh -q '+ r_user+'@'+ip_addr+' exit']
        x=subprocess.call(cmd)
        if x:
            return False
        else:
            return True
    except:
        return False

def get_ip(hostname):
    hostname = hostname.lower()
    # addresses = __salt__['mine.get']('fqdn:'+hostname,'address',expr_form='grain')
    addresses = __salt__['mine.get'](hostname,'address')
    # return addresses
    addresses = addresses[hostname]
    result = None
    for ip_addr in addresses:
        if test_ip_ssh(ip_addr):
            return ip_addr

    return None

def get_role(hostname):
    hostname = hostname.lower()
    # addresses = __salt__['mine.get']('fqdn:'+hostname,'address',expr_form='grain')
    role = __salt__['mine.get'](hostname,'inventory')[hostname]['role']
    return role

#Temporary functions
#TODO: remove all add_*_host wrappers and just use the original add_host() function.
def add_smb_host(hostname, address, username, password):
    backup_arguments = {
        'SmbShareUserName' : username,
        'SmbSharePasswd' : password,
        'FullKeepCnt' : [15, 0, 2, 1, 2, 5, 2],
        'FullPeriod' : 0.97,
        'IncrPeriod' : 10,
        'IncrKeepCnt' : 0,
        'PingCmd' : '/bin/nc -z $host 445',
        'XferMethod' : 'smb',
        'SmbShareName' : []
    }
    return add_host(hostname, address, 'smb', backup_arguments)


def add_minion_host(minion):
    address = get_ip(minion)
    if not address:
        return {"success" : False, "message" : "Minion is unreachable from Backup app", "data" : {}}

    exitcode = add_rsync_host(minion,address)
    if exitcode:
        return exitcode
    return add_default_paths([minion])


def add_rsync_host(hostname, address = None, password = None):
    backup_arguments = {
        'XferMethod' :'rsync',
        'RsyncShareName': []
    }
    if not address:
        address = get_ip(hostname) or hostname

    if password:
        #will use the password to upload ssh key
        exitcode=putkey_windows(hostname, password)
    else:
        #will try to push the key from the master if it is a minion
        exitcode = __salt__['event.send']('backup4/copykey', minion=hostname)
        #return exitcode (always true)
    #lets make real ssh test
    exitcode = test_session_ssh(address, 'root', 'backuppc')
    if not exitcode:
        return {"success" : False, "message" : "Adding SSH key to "+hostname+"("+address+") failed!", "data" : {}}

    exitcode = __salt__['cmd.retcode'](cmd=rm_key+address, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
    if exitcode:
        return {"success" : False, "message" : "Can not remove old SSH keys for "+hostname, "data" : {}}

    exitcode = __salt__['cmd.retcode'](cmd=sshcmd+address+' exit', runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
    if exitcode:
        return {"success" : False, "message" : "Can not add "+hostname+" to the list of known hosts", "data" : {}}

    add_host(hostname, address, 'rsync', backup_arguments)


def add_archive_host(hostname):
    backup_arguments = {
        'XferMethod': 'archive'
    }
    return add_host(hostname, method = 'archive', backup_arguments = backup_arguments)

#backup_arguments is a list of whatever other arugments we want, for instance {"SmbSharePasswd" : "pass", "SmbShareUserName" : "backuppc", "DumpPreUserCmd" : "arg", "DumpPostUserCmd" : "arg"}}
def add_host(hostname, address=None, method='rsync', backup_arguments = {}):

    hostname = hostname.lower()
    if not address:
        address = get_ip(hostname) or hostname

    if not __salt__['file.file_exists'](host_file(hostname)):
        #If the file doesn't exist, we create the full file_data dict.
        file_data = backup_arguments

        file_data['ClientNameAlias'] = address

        #Update backuppc folders
        __salt__['file.chown'](host_file(hostname), 'backuppc', 'www-data')
        __salt__['file.append'](backuppc_hosts, hostname+'       0       backuppc')

        #Finally, we convert the dict to a config file.
        write_dict_to_conf(file_data, hostname)
    else:
        #TODO why is this even here? Looks like it should be in an edit_host function.
        edit_conf_var(hostname, 'ClientNameAlias', str(address))

    __salt__['service.reload']('backuppc')

    return True



def rm_host(hostname):
    #To completely remove a client and all its backups, you should remove its entry in the conf/hosts file, and
    #then delete the __TOPDIR__/pc/$host directory. Whenever you change the hosts file, you should send BackupPC a HUP (-1) signal
    # so that it re-reads the hosts file. If you don't do this, BackupPC will automatically re-read the hosts file at the next regular wakeup.
    hostname = hostname.lower()
    retcode = __salt__['file.remove'](host_file(hostname))
    __salt__['file.line'](path=backuppc_hosts,content=hostname+'.*backuppc', mode='delete')
    __salt__['file.chown'](backuppc_hosts, 'backuppc', 'www-data')
    __salt__['service.reload']('backuppc')
    return retcode

def add_folder(hostname, folder, backup_filter = ""):
    host_conf = conf_file_to_dict(hostname)
    hostname = hostname.lower()

    if folder[-1] == '/':
        folder = folder[:-1]
    if not __salt__['file.file_exists'](host_file(hostname)):
        return 'Host %s not found' % (hostname)
    if __salt__['file.search'](host_file(hostname),'\''+folder+'/?\''):
        return False

    method = get_host_protocol(hostname)
    new_folders = host_conf[method] + [folder]
    edit_conf_var(hostname, method, new_folders)

    if method == 'rsync':
        if __salt__['cmd.retcode'](cmd=sshcmd+get_ip(hostname)+' test ! -d '+folder, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc'):
            return True
        else:
            return False

    if backup_filter:
        add_filter_to_path(hostname, folder, backup_filter)

    __salt__['service.reload']('backuppc')

def add_folder_list(hostname, folder_list):
    for folder in folder_list:
        add_folder(hostname=hostname,folder=folder)

def calculate_backup_periods(full_period, counters, limit):
    if type(counters) != list:
        counters = [counters]
    counters = [int(x) for x in counters]
    full_period = float(full_period)
    full_period = (int((full_period - 0.001) * 24.0) + 1 )/ 24.0
    periods = [0.0]
    for i in range(len(counters)):
        ctr = counters[i]
        period = 2 ** i * full_period
        for j in range(counters[i]):
            new_val = periods[-1] + period
            if new_val <= limit:
                periods.append(new_val)

    periods = [round(x, 2) for x in periods[1:]]
    return periods


def pretty_backup_periods(full_period, counters, limit=999):
    periods = calculate_backup_periods(full_period, counters, limit)
    pcount = len(periods)
    periods = ', '.join([str(x) for x in periods]) + ', '
    periods = periods.replace('.00', '')
    periods = periods.replace('.0, ', ', ')
    periods = periods.rstrip(' ')
    periods = periods.rstrip(',')
    periods = periods + " [" + str(pcount)+" max]"
    return periods


def get_filters_for_host(hostname, path):
    host_conf = conf_file_to_dict(hostname)
    backup_filters = host_conf.get('BackupFilesOnly', {})

    return backup_filters

def manage_host_filter(hostname, path, backup_filter, action = 'add'):
    if not backup_filter:
        return

    backup_filters = get_filters_for_host(hostname, path)

    if action == 'add':
        path_filters = backup_filters.get(path, []) + [backup_filter]
    elif action == 'remove' :
        path_filters = [x for x in backup_filters.get(path, []) if x != backup_filter]

    else:
        raise Exception('Invalid action in manage_host_filter: ' + str(action))

    backup_filters[path] = path_filters

    edit_conf_var(hostname, 'BackupFilesOnly', backup_filters)

def add_filter_to_path(hostname, path, backup_filter):
    return manage_host_filter(hostname, path, backup_filter, 'add')

def rm_filter_from_path(hostname, path, backup_filter):
    return manage_host_filter(hostname, path, backup_filter, 'remove')


def rm_folder(hostname, folder):
    hostname = hostname.lower()
    host_conf = conf_file_to_dict(hostname)
    method = get_host_protocol(hostname)
    if os.path.exists(host_file(hostname)):
        host_conf = conf_file_to_dict(hostname)
        host_folders = host_conf[method]
        host_folders = [x for x in host_folders if x != folder]

        edit_conf_var(hostname, method, host_folders)
        __salt__['file.chown'](host_file(hostname), 'backuppc', 'www-data')
        return True
        #return 'Folder '+folder+' has been deleted from backup list'
    else:
        return 'Folder not in backup list'


def get_folders_from_config(hostname):
    conf_dir = host_file(hostname)
    host_protocol = get_host_protocol(hostname)

    host_config = conf_file_to_dict(hostname)
    folders = host_config.get(host_protocol, [])

    return folders

def list_folders(hostnames):
    folders_list = dict()
    if type(hostnames) == str:
        hostnames = [hostnames]
    for hostname in hostnames:
        folders = get_folders_from_config(hostname)
        folders_list[hostname] = folders
    return folders_list

def panel_list_folders():
    hostnames = listHosts()
    data  = list_folders(hostnames)
    data = [ {'app': key, 'path': v, 'include' : ', '.join(find_matching_shares(key, v))} for key in data for v in data[key] ]
    return data

def listHosts():
    host_list = []
    with open(backuppc_hosts, "r") as h:
        for line in h:
            if '#' not in line and line != '\n':
                word = line.split()
                host_list.append(word[0])
    host_list = [x for x in host_list if get_host_protocol(x) != 'Archive']
    return host_list

def find_matching_shares(host, share_path):
    folders = []
    shares = conf_file_to_dict(host).get('BackupFilesOnly', [])
    for share in shares:
        if fnmatch.fnmatch(share_path, share):
            folders += shares[share]
    return folders

def panel_list_hosts():
    host_list = listHosts()
    host_list = [{'host' : x, 'total_backups': backupTotals(x), 'protocol' : get_host_protocol(x).replace('ShareName', '').lower(), 'address' : conf_file_to_dict(x).get('ClientNameAlias')} for x in host_list]

    host_list = append_host_status(host_list)
    return host_list

def panel_list_schedule():
    host_schedule = listHosts()
    host_schedule = [{'host' : x, 'fullperiod': get_full_period(x), 'fullmax': get_full_max(x),'incrperiod': get_incr_period(x),'incrmax': get_incr_max(x)} for x in host_schedule]
    return host_schedule


def panel_list_sequences():
    host_seq = listHosts()
    host_seq = [{'host' : x, 'fullseq': calc_full_seq(x), 'incrseq': calc_incr_seq(x)} for x in host_seq]
    return host_seq


def calc_full_seq(hostname):
    full_period = conf_file_to_dict(hostname).get('FullPeriod') or get_global_config('FullPeriod')
    full_cnt = conf_file_to_dict(hostname).get('FullKeepCnt') or get_global_config('FullKeepCnt')
    full_age = conf_file_to_dict(hostname).get('FullAgeMax') or get_global_config('FullAgeMax')
    sequence = pretty_backup_periods(full_period, full_cnt,int(full_age))
    return sequence

def calc_incr_seq(hostname):
    incr_period = conf_file_to_dict(hostname).get('IncrPeriod') or get_global_config('IncrPeriod')
    incr_cnt = conf_file_to_dict(hostname).get('IncrKeepCnt') or get_global_config('IncrKeepCnt')
    incr_age = conf_file_to_dict(hostname).get('IncrAgeMax') or get_global_config('IncrAgeMax')
    sequence = pretty_backup_periods(incr_period, incr_cnt,int(incr_age))
    return sequence


def get_full_period(hostname):
    p = conf_file_to_dict(hostname).get('FullPeriod') or pretty_global_config('FullPeriod') + ' *'
    if type(p) == list:
        p = ', '.join([str(x) for x in p])
    return p

def get_incr_period(hostname):
    p = conf_file_to_dict(hostname).get('IncrPeriod') or pretty_global_config('IncrPeriod')+" *"
    if type(p) == list:
        p = ', '.join([str(x) for x in p])
    return p

def get_full_max(hostname):
    p = conf_file_to_dict(hostname).get('FullKeepCnt') or pretty_global_config('FullKeepCnt')+" *"
    if type(p) == list:
        p = ', '.join([str(x) for x in p])
    return p

def get_incr_max(hostname):
    p = conf_file_to_dict(hostname).get('IncrKeepCnt') or pretty_global_config('IncrKeepCnt')+" *"
    if type(p) == list:
        p = ', '.join([str(x) for x in p])
    return p

def append_host_status(host_list):
    bash_cmd = ['/bin/su','-s', '/bin/sh', 'backuppc', '-c','/usr/local/backuppc/bin/BackupPC_serverMesg status hosts']
    #return subprocess.check_output(bash_cmd)
    try:
        text = subprocess.check_output(bash_cmd)
        text = text.split('Got reply: ')[1]
        text = hashtodict(text)['%Status']
        for x in host_list:
            if text[x['host']].get('activeJob', 0) == 1:
                x['status'] = "In progress since "+str(datetime.datetime.fromtimestamp(int(text[x['host']].get('startTime', '0'))).strftime('%Y-%m-%d %H:%M'))
                x['state'] = 'Pending'

                bash2_cmd = ['/bin/su','-s', '/bin/sh', 'backuppc', '-c','/usr/local/backuppc/bin/BackupPC_serverMesg status jobs']
                try:
                    text2 = subprocess.check_output(bash2_cmd)
                    text2 = text2.split('Got reply: ')[1]
                    #clear job output
                    text2 = text2.replace('*::FH','null').replace('\\\"','').replace('\\$','$')
                    # return text2
                    text2 = hashtodict(text2)['%Jobs']
                    filecount = text2[x['host']].get('xferFileCnt', '-')
                    if type(filecount) != int:
                        filecount=0

                    x['error'] = 'Type: '+ text2[x['host']].get('type', '-')+', '  + str(filecount)+' files so far from: '+text2[x['host']].get('shareName', '-')
                    # x['error'] = '-'
                except subprocess.CalledProcessError as e:
                    x['error'] = '-'

            else:
                x['status'] = text[x['host']].get('reason', '-').capitalize()
                x['status'] = x['status'].replace('_', ' ').replace('Reason ','').capitalize()
                x['state'] = 'Critical' if (x['status']!='Nothing to do' and x['status']!='Backup done' and x['status']!='') else 'none'
                x['error'] = text[x['host']].get('error', "-").replace('_', ' ').replace('\$', '$').capitalize()
                if x['error']=='-':
                    x['error']= text[x['host']].get('lastGoodBackupTime','No good backup!')
                    if type(x['error']) == int:
                        x['error']= "Last good backup: " + str(datetime.datetime.fromtimestamp(x['error']).strftime('%Y-%m-%d %H:%M'))

    except subprocess.CalledProcessError as e:
        for x in host_list:
            x['status'] = 'Error reading status'
            x['state'] = 'none'
            x['error'] = text[x['host']].get('error', "-").replace('_', ' ').replace('\$', '$').capitalize()
    return host_list




def panel_statistics():
    # diskusage =__salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /var/lib/backuppc/ -o TARGET').split()[1]]
    #bash_cmd = ['/usr/bin/sudo', '-u','backuppc', '/usr/share/backuppc/bin/BackupPC_serverMesg', 'status' ,'info']

    bash_cmd = ['/bin/su','-s', '/bin/sh', 'backuppc', '-c','/usr/local/backuppc/bin/BackupPC_serverMesg status info']
    try:
        out = subprocess.check_output(bash_cmd)
        text = hashtodict(out)
        statistics = [{'key' : 'Version', 'value': text['Version']},
                {'key' : 'Files in pool', 'value': text['cpool4FileCnt']},
                {'key' : 'Folders in pool', 'value': text['cpool4DirCnt']},
                # Bug reported alrady {'key' : 'Duplicates in pool', 'value': text['cpool4FileCntRep']},
                {'key' : 'Nightly cleanup removed files', 'value': text['cpool4FileCntRm']},
                # {'key' : 'Pool partition used size (GB)', 'value': int(diskusage['used'])/1024/1024},
                # {'key' : 'Pool partition free space (GB)', 'value': int(diskusage['available'])/1024/1024},
                # {'key' : 'Pool partition mountpoint', 'value': diskusage['filesystem']},
                {'key' : 'Pool usage last count (%)', 'value': text['DUDailyMax']},
                {'key' : 'Pool usage yesterday (%)', 'value': text['DUDailyMaxPrev']},
                {'key' : 'Pool size (GB)', 'value': round(int(text['cpool4Kb'])*1.073741824/1024/1024)}] #GiB to GB


    except subprocess.CalledProcessError as e:

        statistics = [{'key' : 'Error reading data', 'value': 'N/A'}]
    return statistics


def panel_disk():
    diskusage =__salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /var/lib/backuppc/ -o TARGET').split()[1]]
    statistics = [{'key' : 'Pool partition used size (GB)', 'value': int(diskusage['used'])/1024/1024},
                    {'key' : 'Pool partition free space (GB)', 'value': int(diskusage['available'])/1024/1024},
                    {'key' : 'Pool partition mountpoint', 'value': diskusage['filesystem']}]
    return statistics

def panel_default_config():
    # cmd = 'cat /etc/backuppc/config.pl'
    sshkey = 'cat /var/lib/backuppc/.ssh/id_rsa.pub'
    text =  __salt__['cmd.run'](sshkey)
    #possible fix for this stupid hack
    # https://stackoverflow.com/questions/1258416/word-wrap-in-an-html-table
    for x in range(len(text)/100):
        y=(x+1)*100+1
        text = text[:y] + ' ' + text[y:]
    full_period = get_global_config('FullPeriod')
    full_cnt = get_global_config('FullKeepCnt')
    incr_period = get_global_config('IncrPeriod')
    incr_cnt = get_global_config('IncrKeepCnt')

    def_config = [{'key' : 'Full backups interval (days)', 'value': full_period},
                {'key' : 'Full backups to keep (max)', 'value': full_cnt},
                {'key' : 'Full backups to keep (min)', 'value': get_global_config('FullKeepCntMin')},
                {'key' : 'Expected Full backups history (days)', 'value': pretty_backup_periods(full_period, full_cnt,int(get_global_config('FullAgeMax')))},
                {'key' : 'Remove full backups older then', 'value': get_global_config('FullAgeMax')},
                {'key' : 'Incremental backups interval (days)', 'value': get_global_config('IncrPeriod')},
                {'key' : 'Incremental backups to keep (max)', 'value': incr_period},
                {'key' : 'Incremental backups to keep (min)', 'value': incr_cnt},
                {'key' : 'Expected Incremental backups history (days)', 'value': pretty_backup_periods(incr_period, incr_cnt,int(get_global_config('IncrAgeMax')))},
                {'key' : 'Remove incremental backups older then', 'value': get_global_config('IncrAgeMax')},
                {'key' : 'SSH Public key (remove spaces)', 'value': text},
                ]

    return def_config




def get_global_config(item, hostname = 'config'):
    perl_simple_element = ['perl','-e', 'require "/etc/backuppc/%s.pl"; print $Conf{%s};' % (hostname, item)]
    perl_complex_element = ['perl', '-MJSON', '-e', 'require "/etc/backuppc/%s.pl"; $json_data = encode_json $Conf{%s}; print $json_data' % (hostname, item)]

    item = subprocess.check_output(perl_simple_element)
    if any([x in item for x in ['ARRAY', 'HASH']]):
        item = json.loads(subprocess.check_output(perl_complex_element))

    return item

def pretty_global_config(item, hostname = 'config'):
    value = get_global_config(item, hostname)
    if type(value) == list:
        value = ', '.join([str(x) for x in value])
    return value


def get_item_from_conf(item, hostname = 'config'):
    host_conf = host_file(hostname)
    with open(host_conf) as f:
        config = f.read()

    #you can probably do some more regexing to get perl values but this seems to work
    item_regex_comment_group = r'(#.*)?'
    item_regex_var_definition = r"\$Conf{%s}\s*=\s*" % item
    item_regex_value_characters = r'([a-zA-Z\/0-9\.\,]*)'
    item_regex_value = "'?%s'?;" % item_regex_value_characters

    item_regex = item_regex_comment_group + item_regex_var_definition + item_regex_value
#    return item_regex
    item = re.findall(item_regex, config)
    item = [x[1] for x in item if '#' not in x[0]] or [None]

    if not item:
        return None

    item = item[0]
    return item

def handle_vars(line):
    if len(line.split(' = ')) > 1:
        line = line.strip()
        return "'%s' = %s" % (line.split(' = ')[0], line.split(' = ')[1])
    return line

def handle_characters(conf, char_map = hash_to_json_characters_map):
    for pair in char_map:
        conf = conf.replace(pair[0], pair[1])
    return conf

def conf_to_json(conf):

    conf = conf.split('\n')
    conf = '\n'.join([handle_vars(x) for x in conf])
    conf = handle_characters(conf)

    conf = '{%s}' % (conf[:-1]) #[-1] to remove the final comma left after replacing ';' with ','
    conf = json.loads(conf)
    if any(['Got reply' in x for x in conf.keys()]): #Some outputs have the form: `Got reply: %Info : ...` which we want to filter out and just return a nice dictionary
        conf_key = conf.keys()[0]
        conf = conf[conf_key]
    conf = {re.sub(r'\$Conf\{(.*)\}', r'\g<1>', x) : conf[x] for x in conf} #Replace '$Conf{var}' with 'var' to make it more readable

    return conf


hashtodict = conf_to_json

def dict_to_conf(json_data):
    json_data = '\n'.join(["$Conf{%s} = %s;" % (x, json.dumps(json_data[x])) for x in json_data])
    json_data = handle_characters(json_data, char_map = json_to_hash_characters_map)
    return json_data


def file_to_dict(file_path):
    with open(file_path) as f:
        conf = f.read()

    conf = conf_to_json(conf)

    #Some values are 0s which makes it annoying to deal with type checking
    #So we convert all integer 0s to strings.
    conf = {x : conf[x] if conf[x]!= 0 else '0' for x in conf}
    return conf

def conf_file_to_dict(hostname):
    conf_file = host_file(hostname)
    return file_to_dict(conf_file)

def write_dict_to_conf(data, hostname):
    data = dict_to_conf(data)
    conf_file = host_file(hostname)
    with open(conf_file, 'w') as f:
        f.write(data)

def edit_conf_var(hostname, var, new_data, data_type = None):
    conf_data = conf_file_to_dict(hostname)

    if new_data is None:
        if var in conf_data.keys():
            conf_data.pop(var)

    else:
        if data_type and type(var) != data_type:
            try:
                if data_type == list:
                    new_data = [x.strip() for x in new_data.split(',')]
                else:
                    new_data = data_type(new_data)
            except Exception as e:
                raise Exception("Error converting conf var " + str(new_data) + " to data_type " + str(data_type) + ": " + e.message)

        conf_data[var] = new_data
    return write_dict_to_conf(conf_data, hostname)


def change_address(hostname, new_data, var="ClientNameAlias"):
    return edit_conf_var(hostname, var, new_data, data_type = str)

def change_password(hostname, new_data, var="SmbSharePasswd"):
    return edit_conf_var(hostname, var, new_data, data_type = str)



def change_fullperiod(hostname, new_data, var="FullPeriod"):
    return edit_conf_var(hostname, var, new_data, data_type = float)

def change_fullmax(hostname, new_data, var="FullKeepCnt"):
    return edit_conf_var(hostname, var, new_data, data_type = list)


#edit_conf_var hostname "FullKeepCnt" ['15', '0', '2', '1', '2', '5', '2'] data_type = list

def change_incrperiod(hostname, new_data, var="IncrPeriod"):
    return edit_conf_var(hostname, var, new_data, data_type = float)

def change_incrmax(hostname, new_data, var="IncrKeepCnt"):
    return edit_conf_var(hostname, var, new_data, data_type = int)

def reset_schedule(hostname):
    protocol = get_host_protocol(hostname)
    default_values = (None, ) * 4
    if protocol == 'SmbShareName':
        default_values = (0.97, '15, 0, 2, 1, 2, 5, 2', 10, '0')
    if protocol == 'RsyncShareName':
        pass
#       default_values = (1, ['15', '0', '2', '1', '2', '5', '2'], 10, '0')  #Redosled e: (FullPeriod, FullMax, IncrPeriod, IncrMax)

    change_fullperiod(hostname, default_values[0])
    change_fullmax(hostname, default_values[1])
    change_incrperiod(hostname, default_values[2])
    change_incrmax(hostname, default_values[3])
    return "Schedule is set to recommended values for specified protocol"


def backupTotals(hostname):
    totalb = len(backupNumbers(hostname))
    return totalb


def get_host_protocol(hostname = 'config'):
    host_conf = conf_file_to_dict(hostname)
    method = host_conf.get('XferMethod') or get_global_config('XferMethod')
    method_vars = {
        'rsync' : 'RsyncShareName',
        'smb' : 'SmbShareName',
        'archive' : 'Archive',
    }
    protocol = method_vars[method]

    return protocol


def backupNumbers(hostname):
    hostname = hostname.lower()
    limit = re.compile("^[0-9]*$")
    hostname_path = '/var/lib/backuppc/pc/'+hostname+'/'
    if not os.path.isdir(hostname_path):
        return []

    dirs = [d for d in os.listdir(hostname_path) if os.path.isdir(os.path.join(hostname_path, d)) and limit.match(d)]
    return dirs

def backupFiles(hostname, number = -1):
    hostname = hostname.lower()
    if number == -1:
        result = map(int, backupNumbers(hostname))
        number = max(result)
        path = '/var/lib/backuppc/pc/'+hostname+'/'+ str(number) +'/'
    else :
        path = '/var/lib/backuppc/pc/'+hostname+'/'+ str(number) + '/'
    path = os.path.normpath(path)
    ffolders = []
    subfolders = []
    for root,dirs,files in os.walk(path, topdown=True):
        depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
        if depth == 2:
            # We're currently two directories in, so all subdirs have depth 3
            subfolders += [os.path.join(root, d) for d in dirs]
            dirs[:] = [] # Don't recurse any deeper or comment this line for deeper
            # depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
            # if depth == 3:
            #   subfolders += [os.path.join(root, d) for d in dirs]
            #   dirs[:] = []
    for value in subfolders:
        ffolders.append(value.replace('%2f','/'))
    return ffolders

def start_backup(hostname, tip='Full'):
    hostname = hostname.lower()
    if tip == 'Inc':
        tip = '0'
    elif tip == 'Full' or tip is None:
        tip = '1'
    cmd = '/usr/local/backuppc/bin/BackupPC_serverMesg backup '+hostname+' '+hostname+' backuppc '+tip
    return __salt__['cmd.run'](cmd, runas='backuppc')


def delete_backup(hostname, tip='Full'):
    hostname = hostname.lower()
    if tip == 'Inc':
        tip = '0'
    elif tip == 'Full' or tip is None:
        tip = '1'
        # /usr/bin/perl /usr/local/BackupPC/bin/BackupPC_backupDelete -h i3 -n 7 -l
    cmd = '/usr/local/backuppc/bin/BackupPC_serverMesg backup '+hostname+' '+hostname+' backuppc '+tip
    return __salt__['cmd.run'](cmd, runas='backuppc')

def start_backup_incr(hostname, tip='Inc'):
    start_backup(hostname, tip)

def create_archive(hostname):
    protocol = get_host_protocol(hostname)
    if protocol == 'Archive' :
        return "Cannot create archive on host %s: Protocol for the host is archive. " % (hostname)
    cmd = '/usr/local/backuppc/bin/BackupPC_archiveStart archive backuppc %s' % (hostname)
    result = __salt__['cmd.run'](cmd, runas = 'backuppc')
    return result

def putkey_windows(hostname, password, username='root', port=22):
    hostname = hostname.lower()
    cmd1 = 'sshpass -p '+password+' ssh-copy-id -oStrictHostKeyChecking=no '+username+'@'+hostname+ ' -p '+str(port)
    cmd = 'sshpass -p '+password+' ssh -oStrictHostKeyChecking=no '+username+'@'+hostname+ ' -p '+str(port)+' bash -l &'
    __salt__['cmd.run'](cmd, runas='backuppc')
    return __salt__['cmd.run'](cmd1, runas='backuppc')

def dir_structure(hostname, number = -1, rootdir = '/var/lib/backuppc/pc/'):
    hostname = hostname.lower()
    try:
        len(backupNumbers(hostname)) > 0
    except:
        return "No files available."
    hostname = hostname.lower()
    if len(backupNumbers(hostname)) == 0:
        rootdir = '/var/lib/backuppc/pc/'+hostname+'/'
    elif number == -1:
        result = map(int, backupNumbers(hostname))
        number = max(backupNumbers(hostname))
        rootdir = '/var/lib/backuppc/pc/'+hostname+'/'+str(number)+'/'
    else :
        rootdir = '/var/lib/backuppc/pc/'+hostname+'/'+str(number)+'/'
    dr = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    struktura = os.walk(rootdir)

    def filter_f(name):
        BLACKLIST = ('attrib', 'backupInfo', 'backupInfo.json')
        if len(name) > 0 and name[0] == 'f' and name not in BLACKLIST:
            return name[1:]
        else:
            return name

    for path, dirs, files in struktura:
        new_path = [filter_f(part) for part in path.split(os.sep)]
        path = os.sep.join(new_path)
        folders = path[start:].split(os.sep) # /pateka/vo/momentov
        subdir = {filter_f(a):None for a in files}
        parent = reduce(dict.get, folders[:-1], dr) # dr.get(folders[0]).get(folders[1]) ... roditelot
        parent[folders[-1]] = subdir # roditel[sin] = subdir

    if len(dr.keys()):
        first_key = dr.keys()[0]
        first_val = dr[first_key]
        if isinstance(first_val, dict):
            dr = first_val

    for key, val in dr.items():
        del dr[key]
        dr[key.replace('%2f', '/')] = val

    return dr

def write_backupinfo_json(hostname, backup):
    hostname = hostname.lower()
    contents = ''
    path = get_path_from_backup_number(hostname, backup)
    with open(path + '/backupInfo','r+') as f:
        contents = f.read()
        contents = hashtodict(contents)
    with open(path + '/backupInfo.json', 'w') as f:
        json.dumps(f.write(contents))

def backup_info(hostname):
    hostname = hostname.lower()
    backup_list = backupNumbers(hostname)
    content = []
    for backup in backup_list:
        info = {}
#        write_backupinfo_json(hostname, str(backup))
        json_path = get_path_from_backup_number(hostname, backup) + '/backupInfo'

        json_data = file_to_dict(json_path)['%backupInfo']

        #TODO proper handling of these cases.

        # handle craziness


        try:
            json_data["startTime"]=int(json_data["startTime"])
        except:
            json_data["startTime"]=0


        try:
            json_data["endTime"]=int(json_data["endTime"])
        except:
            json_data["endTime"]=-1


        try:
            json_data["sizeNew"]=int(json_data["sizeNew"])
        except:
            json_data["sizeNew"]=0


        try:
            json_data["size"]=int(json_data["size"])
        except:
            json_data["size"]=0

        # return json_data

        if 'startTime' in json_data:
            info["startTime"] = str(datetime.datetime.fromtimestamp(json_data["startTime"]).strftime('%Y-%m-%d %H:%M'))
        else:
            info["startTime"] = 'unknown'

        if 'startTime' in json_data and 'endTime' in json_data:
            if json_data["endTime"] > json_data["startTime"]:
                info["duration"] = str(datetime.timedelta(seconds = (json_data["endTime"] - json_data["startTime"])))
                info["endTime"] = str(datetime.datetime.fromtimestamp(json_data["endTime"]).strftime('%Y-%m-%d %H:%M'))
            else:
                info["duration"] = '-'
                info["endTime"] = 'unknown'
        if 'sizeNew' in json_data:
            info["sizeNew"] = bytes_to_readable(json_data["sizeNew"])
        else:
            info["sizeNew"] = 'unknown'

        if 'size' in json_data:
            info["size"] = bytes_to_readable(json_data["size"])
        else:
            info["size"] = 'unkown'
        info["type"] = json_data["type"]

        if 'endTime' in json_data:
            a = int(time.time()) - json_data["endTime"]
            m, s = divmod(a, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            if a > 0 and json_data["endTime"]>-1:
                info.update({
                    "age" : str("%d day(s) %d:%02d") % (d, h, m),
                    "backup" : str(backup),
                    # "absolute_age" : a
                })
            else:
                info.update({
                "age" : '-',
                "backup" : str(backup),
                # "absolute_age" : a
            })
        else:
            info.update({
                "age" : 'active',
                "backup" : str(backup),
                # "absolute_age" : a
            })
        #NOPE #info["age"] = str(datetime.timedelta(seconds = (int(time.time()) - int(f["endTime"]))))
        content.append(info)
    content = sorted(content, key = lambda x: x['startTime'], reverse = True)
    return content

def backup_info_graph_old(hostname):
    #try to calculate size for incr backups
    hostname = hostname.lower()
    backup_list = backupNumbers(hostname)
    content = []
    last_full_size = 0
    backup_list = sorted(backup_list) #, key = lambda x: x['startTime'], reverse = False)
    for backup in backup_list:
        info = {}
        json_path = get_path_from_backup_number(hostname, backup) + '/backupInfo'

        json_data = file_to_dict(json_path)['%backupInfo']

        #TODO proper handling of these cases.
        if 'startTime' in json_data:
            info["startTime"] = str(datetime.datetime.fromtimestamp(int(json_data["startTime"])).strftime('%Y-%m-%d %H:%M'))
            info["startTimeStamp"] = int(json_data["startTime"])
        if json_data["type"]=="full":
            last_full_size=int(json_data["size"])
            info["sizeGraph"] = last_full_size/1024/1024
        else:
            last_full_size = last_full_size+int(json_data["sizeNew"])
            info["sizeGraph"] = (last_full_size)/1024/1024
        content.append(info)
    #content = sorted(content, key = lambda x: x['startTime'], reverse = False)
    return content


def backup_info_graph(hostname):
    #make graphs from full backups only
    hostname = hostname.lower()
    backup_list = backupNumbers(hostname)
    content = []
    #last_full_size = 0
    #backup_list = sorted(backup_list) #, key = lambda x: x['startTime'], reverse = False)
    for backup in backup_list:
        info = {}
        json_path = get_path_from_backup_number(hostname, backup) + '/backupInfo'

        json_data = file_to_dict(json_path)['%backupInfo']

        #TODO proper handling of these cases.
        if json_data["type"]=="full":
            if 'startTime' in json_data:
                info["startTime"] = str(datetime.datetime.fromtimestamp(int(json_data["startTime"])).strftime('%Y-%m-%d %H:%M'))
                info["startTimeStamp"] = int(json_data["startTime"])
                info["sizeGraph"] = (int(json_data["size"]))/1024/1024
                content.append(info)
    content = sorted(content, key = lambda x: x['startTime'], reverse = False)
    return content


def tar_create(arguments, location='/usr/share', backupname='test_backup', backupnumber=-1):
    tar_create_cmd = '/usr/share/backuppc/bin/BackupPC_tarCreate -h '+arguments[0]+' -s '+arguments[1]+' -n '+str(backupnumber)+' '+arguments[2]+' > '+location+'/'+backupname+'.tar'
    return __salt__['cmd.run'](tar_create_cmd ,runas='backuppc', cwd='/var/lib/backuppc',python_shell=True)


#Example url
#http://10.0.10.45/index.cgi?action=RestoreFile&host=serversql&num=47&share=/cygdrive/c/db-dump&dir=/TEST_backup_2017_09_13_161329_0384659.fbak

def get_backuppc_url(hostname, backupnumber, share, path, action = 'RestoreFile', username = 'admin', password = '', instance_url = ''):
    kwargs = {
        'hostname' : hostname,
        'backupnumber' : backupnumber,
        'share' : share,
        'path' : path,
        'action' : action,
        'username' : username,
    }

    kwargs['password'] = password or __salt__['pillar.get']('admin_password')
    kwargs['instance_url'] = instance_url or __salt__['network.ip_addrs']()[0]

    url = 'http://{username}:{password}@{instance_url}/index.cgi?action={action}&host={hostname}&num={backupnumber}&share={share}&dir={path}'

    url = url.format(**kwargs)
    return url


def download_zip(hostname, backupnumber = -1, share = '', path = '.', range_from = 0):
    zip_create_cmd = '/usr/share/backuppc/bin/BackupPC_zipCreate'
    p = subprocess.Popen(['sudo', '-u', 'backuppc', zip_create_cmd, '-h', hostname, '-n', str(backupnumber),
        '-s', share, ' ', path], stdout=subprocess.PIPE)
    BLOCK_SIZE = 10 ** 6
    has_read = 0
    while True:
        curr_out = p.stdout.read(BLOCK_SIZE)
        current_read = len(curr_out)
        has_read+= current_read
        if curr_out == '': return ''
        if has_read > range_from:
            return curr_out[range_from % BLOCK_SIZE:]

def restore_backup(hostname, backupnumber = -1, share = '',  path = '.', restore_host=''):
    if restore_host == '':
        restore_host=hostname
    protocol = get_host_protocol(hostname)
    tar_create_cmd = '/usr/share/backuppc/bin/BackupPC_tarCreate'

    if protocol == 'SmbShareName':
        address = conf_file_to_dict(restore_host).get('ClientNameAlias') or hostname
        user = conf_file_to_dict(hostname).get('SmbShareUserName')
        winpass = conf_file_to_dict(hostname).get('SmbSharePasswd')
        args = ' -h '+hostname+' -n '+str(backupnumber)+' -s \''+share+'\' \''+path+'\' | /usr/bin/smbclient \'\\\\' +address+'\\'+share+'\' -U '+user+'%'+winpass+'  -E -d 5 -c tarmode\ full -Tx -'
        #args = ' -h '+hostname+' -n '+str(backupnumber)+' -s '+share+' '+path+' | /usr/bin/smbclient \'\\' +restore_host+share'  -E -d 6 -c tarmode\ full -Tx -'
        __salt__['cmd.run'](tar_create_cmd+args,runas='backuppc', cwd = '/usr/lib/backuppc/',python_shell=True)
        return "Restoring..."

    elif protocol == 'RsynchareName':
        args = ' -h '+hostname+' -n '+str(backupnumber)+' -s '+share+' '+path+' | ssh root@'+restore_host+' tar xf - -C '+share
        return __salt__['cmd.run'](tar_create_cmd+args,runas='backuppc', cwd = '/usr/lib/backuppc/',python_shell=True)

#This is a temporary 'hack', until we figure out what we really want to do.
restore = restore_backup

#def restore(arguments, restore_host='', backupnumber=-1):
#    hostname = arguments[0]
#    share = arguments[1]
#    path = arguments[2]
#    return restore_backup(hostname, share, path, restore_host, backupnumber)

def infodict(path):
    contents = ''
    cmd = 'sudo -u backuppc /usr/share/backuppc/bin/BackupPC_attribPrint \'%s/attrib\' > \'%s/attrib0\'' % (path, path)
    # cmd = ['sudo -u ', 'backuppc', '/usr/share/backuppc/bin/BackupPC_attribPrint '+path+'/attrib', '>', path+'/attrib0'
    subprocess.call(cmd, shell = True)
    conf = file_to_dict(path + '/attrib0')

#    with open(path +'/attrib0','r+') as f:
#        contents = f.read()
#        contents = contents.replace('$VAR1 = {\n' , '{')
#        contents = contents.replace('}\n}', '}}')
#        contents = contents.replace('=>', ':')
#        contents = contents.replace('%','')
#        contents = contents.replace('\'','\"')
#        contents = contents.replace('(','{')
#        contents = contents.replace(')','}')
#        contents = contents.replace(';','')

    contents = json.dumps(conf.get('$VAR1', {})) or '{}'
    with open(path+'/attrib.json', 'w') as f:
        json.dumps(f.write(contents))

def backup_attrib(hostname, number, *args):
    start = '/var/lib/backuppc/pc/'
    newshare ='empty'
    share = ''
    path = ''
    try:
        len(backupNumbers(hostname)) > 0
    except:
        return "No files available."
    if len(args) == 1:
        share = args[0]
        share = 'f' + share.replace('/','%2f')
        path = ''
    elif len(args) >= 2:
        share = args[0]
        share = 'f' + share.replace('/','%2f')
        path = '/' + '/'.join(args[1:])
        path = path.replace('/', '/f')
#    return "Calling " + start+hostname+'/'+str(number)+'/'+share+path
    infodict(start+hostname+'/'+str(number)+'/'+share+path)
    content = {}

    attrib_file = start + hostname + '/' + str(number) + '/' + share + path + '/attrib.json'
    with open(attrib_file) as f:
        f = f.read()
        f = json.loads(f)

    for key in f:
        name = key
        for keykey in f[key]:
            if keykey == 'mtime':
                time = datetime.datetime.fromtimestamp(int(f[key][keykey])).strftime('%Y-%m-%d %H:%M:%S')
            elif keykey == 'size':
                size = f[key][keykey]
        #info = { 'name' : name, 'time' : time, 'size' : size}
        content[name] = {'time' : time, 'size' : size}
    os.remove(start+hostname+'/'+str(number)+'/'+share+path+'/attrib.json')
    os.remove(start+hostname+'/'+str(number)+'/'+share+path+'/attrib0')
    return content
