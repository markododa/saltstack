import va_utils, salt, os.path, os, json, datetime, time, re, subprocess
from va_utils import check_functionality as panel_check_functionality
from va_backup_panels import panel

sshcmd='ssh -oStrictHostKeyChecking=no root@'
rm_key='ssh-keygen -f "/var/lib/backuppc/.ssh/known_hosts" -R '

default_paths = {
    'va-monitoring' : ['/etc/icinga2', '/root/.va/backup', '/var/lib/pnp4nagios/perfdata/'],
    'va-directory' : ['/root/.va/backup', '/etc/openvpn'],
    'va-backup' : ['/etc/backuppc'],
    'va-fileshare' : ['/home', '/etc/samba'],
    'va-email' : ['/etc/postfix', '/root/.va/backup', '/var/vmail/'],
    'va-owncloud' : ['/root/.va/backup', '/var/www/owncloud'],
}

#def get_panel(panel_name, host = '', backupNum = -1):
def get_panel(panel_name, server_name = '', backupNum = -1):
    host = server_name
    ppanel = panel[panel_name]
    hostnames = __salt__['backuppc.listHosts']()
    if panel_name == "backup.hosts":
        ppanel['tbl_source']['table'] = panel_list_hosts()
        return ppanel

    elif panel_name == "backup.manage":
        data  = list_folders(hostnames)
        data = [ {'app': key, 'path': v} for key,val in data.items() for v in val ]
        ppanel['tbl_source']['table'] = data
        return ppanel

    elif panel_name == "backup.browse":
        host = hostnames[0] if host == '' else host
        if backupNum == -1:
            backupNum = last_backup(host)
        data = dir_structure1(host, backupNum)
        ppanel['form_source'] = {"dropdown": {}};
        ppanel["form_source"]["dropdown"]["values"] = hostnames
        ppanel["form_source"]["dropdown"]["select"] = host
        ppanel['tbl_source']['table'] = data
        ppanel['tbl_source']['path'] = [host, backupNum]
        return ppanel

    elif panel_name == "backup.info":
        data = backup_info(host)
        ppanel['tbl_source']['table'] = data
        return ppanel

def dir_structure1(host, *args):
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
        size = time = '/'
        if key in attrib:
            a = attrib[key]
            size, time = (a['size'], a['time'])
        if size != '/' and time != '/': 
            result.append({'dir': key, 'type': type, 'size': size, 'time': time});
    if check:
        return {'val': backupNum, 'list': result}
    [d.update({'size' : ''}) for d in result if d['type'] == 'folder']
    return result

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
        paths = [default_paths[x] for x in default_paths if __salt__['mine.get'](x, 'inventory')[x]['fqdn'] == host][0]
        for path in paths:
            result = add_folder(host, path)
    return True

def get_ip(hostname):
    hostname = hostname.lower()
    address = __salt__['mine.get']('fqdn:'+hostname,'address',expr_form='grain')
    return address[address.keys()[0]][0]

def add_host(hostname,address=False,method='rsync',scriptpre="None",scriptpost="None"):
        rsync = '$Conf{XferMethod} = \'rsync\';\n$Conf{RsyncShareName} = [\n];'
        methods = { 'rsync': rsync ,}
	hostname = hostname.lower()
	if not __salt__['file.file_exists']('/etc/backuppc/pc/'+hostname+'.pl'):
		#hosts_file_add(hostname,address)
    		__salt__['file.write'](path='/etc/backuppc/pc/'+hostname+'.pl', args=methods[method])
    		__salt__['file.append'](path='/etc/backuppc/pc/'+hostname+'.pl', args='$Conf{ClientNameAlias} = '+get_ip(hostname)+';')
    		__salt__['file.chown']('/etc/backuppc/pc/'+hostname+'.pl', 'backuppc', 'www-data')
    		__salt__['file.append']('/etc/backuppc/hosts', hostname+'       0       backuppc')
        	__salt__['event.send']('backuppc/copykey', fqdn=hostname)
                __salt__['cmd.retcode'](cmd=rm_key+hostname, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
                __salt__['cmd.retcode'](cmd=sshcmd+hostname+' exit', runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
		if scriptpre != "None":
			__salt__['file.append']('/etc/backuppc/pc/'+hostname+'.pl','$Conf{DumpPreUserCmd} = \'$sshPath -q -x -l root $host '+scriptpre+'\';')
		if scriptpost != "None":
			__salt__['file.append']('/etc/backuppc/pc/'+hostname+'.pl','$Conf{DumpPostUserCmd} = \'$sshPath -q -x -l root $host '+scriptpost+'\';')
	return True

# $Conf{ClientCharset} = 'cp1252';
# $Conf{RsyncShareName} = [
  # '/cygdrive/c/VapourApps/Backup'
# ];
# $Conf{XferMethod} = 'rsync';
# SCRIPT PRERUN FOR MSSQLEXPRESS
# $Conf{DumpPreUserCmd} = '$sshPath -q -x -l SvcCOPSSH $host /cygdrive/c/VapourApps/DBbackup.bat';
# $Conf{RsyncClientCmd} = '$sshPath -q -x -l SvcCOPSSH $host $rsyncPath $argList+';
# $Conf{RsyncClientPath} = '/cygdrive/c/VapourApps/rsyncd/bin/rsync';
# $Conf{RsyncClientRestoreCmd} = '$sshPath -q -x -l SvcCOPSSH $host $rsyncPath $argList+';


def rm_host(hostname):
    #To completely remove a client and all its backups, you should remove its entry in the conf/hosts file, and then delete the __TOPDIR__/pc/$host directory. Whenever you change the hosts file, you should send BackupPC a HUP (-1) signal so that it re-reads the hosts file. If you don't do this, BackupPC will automatically re-read the hosts file at the next regular wakeup.
    hostname = hostname.lower()
    retcode = __salt__['file.remove']('/etc/backuppc/pc/'+hostname+'.pl')
    __salt__['file.line'](path='/etc/backuppc/hosts',content=hostname+'.*backuppc', mode='delete')
    __salt__['file.chown']('/etc/backuppc/hosts', 'backuppc', 'www-data')
    __salt__['service.reload']('backuppc')
    return retcode

def add_folder(hostname, folder,address=False,method='rsync',scriptpre="None",scriptpost="None"):
    hostname = hostname.lower()
    if folder[-1] == '/':
        folder = folder[0:-1]
    if not __salt__['file.file_exists']('/etc/backuppc/pc/'+hostname+'.pl'):
	    add_host(hostname=hostname,address=address,scriptpre=scriptpre,scriptpost=scriptpost,method=method)
    if __salt__['file.search']('/etc/backuppc/pc/'+hostname+'.pl','\''+folder+'/?\''):
		return False
    elif __salt__['cmd.retcode'](cmd=sshcmd+hostname+' test ! -d '+folder, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc'):
        __salt__['file.replace']('/etc/backuppc/pc/'+hostname+'.pl', pattern="\$Conf\{RsyncShareName\} \= \[", repl="$Conf{RsyncShareName} = [\n  '"+folder+'\',')
        __salt__['service.reload']('backuppc')
        return True
    else:
        return False

def add_folder_list(hostname, folder_list,address, method='rsync',scriptpre="None",scriptpost="None"):
	for folder in folder_list:
		add_folder(hostname=hostname,folder=folder,address=address,method=method,scriptpre=scriptpre,scriptpost=scriptpost)

def rm_folder(hostname, folder):
    hostname = hostname.lower()
    if os.path.exists('/etc/backuppc/'+hostname+'.pl') and __salt__['file.line'](path='/etc/backuppc/pc/'+hostname+'.pl',content='\''+folder,mode='delete'):
        __salt__['file.chown']('/etc/backuppc/pc/'+hostname+'.pl', 'backuppc', 'www-data')
        if list_folders([hostname])[hostname] == []:
            rm_host(hostname)
        return 'Folder '+folder+' has been deleted from backup list'
    else:
        return 'Folder not in backup list'

#def backup_count():


def list_folders(hostnames):
	folders_list = dict()
	if type(hostnames) == str:
		hostname = hostnames
		hostnames = []
		hostnames.append(hostname)
	for hostname in hostnames:
		folders = []
		if os.path.exists('/etc/backuppc/'+hostname+'.pl'):
			config_file = open('/etc/backuppc/'+hostname+'.pl', 'r').read().splitlines()
			for folder in config_file[config_file.index('$Conf{RsyncShareName} = [')+1:config_file.index('];')]:
				folders.append(folder.split('\'')[1])
		folders_list[hostname] = folders
	return folders_list

def listHosts():
    host_list = []
    with open("/etc/backuppc/hosts", "r") as h:
        for line in h:
            if '#' not in line and line != '\n':
                word = line.split()
                host_list.append(word[0])
    return host_list

def panel_list_hosts():
    host_list = listHosts()
    host_list = [{'host' : x, 'total_backups': backupTotals(x)} for x in host_list]
    return host_list


def panel_statistics():
    cmd = '/usr/share/backuppc/bin/BackupPC_serverMesg status info'
    text =  __salt__['cmd.run'](cmd, runas='backuppc')
    text = hashtodict(text)
    text = text.split('=')[1]
    text = json.loads(text)
    i_version = text['Version']
    i_todaypool = text['DUDailyMax']
    i_yesterdaypool = text['DUDailyMaxPrev']
    i_folders = text['cpoolDirCnt']
    i_duplicates = text['cpoolFileCntRep']
#"cpoolFileCnt" => 25690          files in pool
#"cpoolDirCnt" => 4368,          directories in pool
#"cpoolFileCntRep" => 0               repeated files
    statistics = [{'key' : 'Version', 'value': text['Version']},
		  {'key' : 'Files in pool', 'value': text['cpoolFileCnt']},
		  {'key' : 'Folders in pool', 'value': text['cpoolDirCnt']},
		  {'key' : 'Duplicates in pool', 'value': text['cpoolFileCntRep']},
		  {'key' : 'Nightly cleanup removed files', 'value': text['cpoolFileCntRm']},
		  {'key' : 'Pool used size (KB)', 'value': __salt__['disk.usage']()['/mnt/va-backup']['used']},
		  {'key' : 'Pool free space (KB)', 'value': __salt__['disk.usage']()['/mnt/va-backup']['available']},
		  {'key' : 'Pool files system', 'value': __salt__['disk.usage']()['/mnt/va-backup']['filesystem']},
		  {'key' : 'Pool usage now (%)', 'value': text['DUDailyMax']},
		  {'key' : 'Pool usage yesterday (%)', 'value': text['DUDailyMaxPrev']}]
    return statistics


def backupTotals(hostname):
    totalb = len(backupNumbers(hostname)) 
    return totalb


def backupNumbers(hostname):
    hostname = hostname.lower()
    limit = re.compile("^[0-9]*$")
    dirs = [d for d in os.listdir('/var/lib/backuppc/pc/'+hostname+'/') if os.path.isdir(os.path.join('/var/lib/backuppc/pc/'+hostname+'/', d)) and limit.match(d)]
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

def start_backup(hostname, tip='Inc'):
    hostname = hostname.lower()
    if tip == 'Inc':
        tip = '0'
    elif tip == 'Full':
        tip = '1'
    cmd = '/usr/share/backuppc/bin/BackupPC_serverMesg backup '+hostname+' '+hostname+' backuppc '+tip
    return __salt__['cmd.run'](cmd, runas='backuppc')

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

def hashtodict(contents):
    contents = contents.replace('=>', ':')
    contents = contents.replace('%','')
    contents = contents.replace('\'','\"')
    contents = contents.replace('(','{')
    contents = contents.replace(')','}')
    contents = contents.replace(';','')
    contents = contents.replace('backupInfo = ','')
    contents = contents.replace('\"fillFromNum\" : undef,','')
    return contents

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
        write_backupinfo_json(hostname, str(backup))
        json_path = get_path_from_backup_number(hostname, backup)

        f = json.loads(open(json_path + '/backupInfo.json').read())
        for key in f:
            if key == "startTime":
                info.update({"startTime" : str(datetime.datetime.fromtimestamp(int(f["startTime"])).strftime('%Y-%m-%d %H:%M:%S')) })
            elif key == "endTime":
                info.update({"endTime" : str(datetime.datetime.fromtimestamp(int(f["endTime"])).strftime('%Y-%m-%d %H:%M:%S'))})
            elif key == "type":
                info.update({"type" : f["type"]})
            info.update({"duration" : str(datetime.timedelta(seconds = (int(f["endTime"]) - int(f["startTime"]))))})
            a = int(time.time()) - int(f["endTime"])
            m, s = divmod(a, 60)
            h, m = divmod(m, 60)
            info.update({
                "age" : str("%d:%02d:%02d") % (h, m, s),
                "backup" : str(backup),
                "absolute_age" : str(a)
            })
        #info["age"] = str(datetime.timedelta(seconds = (int(time.time()) - int(f["endTime"]))))
        content.append(info)
        os.remove(json_path + '/backupInfo.json')
    content = sorted(content, key = lambda x: x['startTime'], reverse = True)
    return content

def tar_create(arguments, location='/usr/share', backupname='test_backup', backupnumber=-1):
    tar_create_cmd = '/usr/share/backuppc/bin/BackupPC_tarCreate -h '+arguments[0]+' -s '+arguments[1]+' -n '+str(backupnumber)+' '+arguments[2]+' > '+location+'/'+backupname+'.tar'
    return __salt__['cmd.run'](tar_create_cmd ,runas='backuppc', cwd='/var/lib/backuppc',python_shell=True)

def fake_download(range_from):
    class A(object): pass
    p = A()
    import StringIO
    p.stdout = StringIO.StringIO('zdravo jas sum filip')
    BLOCK_SIZE = 3
    has_read = 0
    while True:
        curr_out = p.stdout.read(BLOCK_SIZE)
        current_read = len(curr_out)
        has_read+= current_read
        if curr_out == '': return ''
        if has_read > range_from:
            return curr_out[range_from % BLOCK_SIZE:]


#Example url
#http://10.0.10.45/index.cgi?action=RestoreFile&host=serversql&num=47&share=/cygdrive/c/db-dump&dir=/TEST_backup_2017_09_13_161329_0384659.fbak
#
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
    tar_create_cmd = '/usr/share/backuppc/bin/BackupPC_tarCreate'
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
    with open(path +'/attrib0','r+') as f:
        contents = f.read()
        contents = contents.replace('$VAR1 = {\n' , '{')
        contents = contents.replace('}\n}', '}}')
        contents = contents.replace('=>', ':')
        contents = contents.replace('%','')
        contents = contents.replace('\'','\"')
        contents = contents.replace('(','{')
        contents = contents.replace(')','}')
        contents = contents.replace(';','')

    contents = contents or '{}'
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
    elif len(args) == 2:
        share = args[0]
        share = 'f' + share.replace('/','%2f')
        path = '/' + args[1]
        path = path.replace('/', '/f')
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
