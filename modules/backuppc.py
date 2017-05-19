import salt, os.path

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

panel = {"title":"All backups","content":[{"type":"MultiTable","name":"div","reducers":["table"],"elements":[{"type":"Form","name":"form","class":"pull-right margina","args":{"hostname":""},"elements":[{"type":"Button","name":"Add Backup","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add a backup","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add backup","class":"primary","action":"add_folder"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"backup_path","value":"","label":"Backup path","required":True},]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to add a new backup"},{"type":"Paragraph","name":"Enter the full absolute path to the backup. The file must exist."}]},]}}]},{"type":"Table","reducers":["table","panel","alert"],"columns":[{"key":"","label":""},{"key":"action","label":"Actions"}],"actions":[{"name":"Remove backup","action":"rm_folder"}],"id":""}]}]}

def get_panel(panel_name):
    hostnames = ['va-monitoring', 'va-directory', 'va-backup', 'va-fileshare']
    data  = list_folders(hostnames)
    data = { key: val for key,val in data.items()}
    panel['tbl_source'] = data
    return panel

def add_default_paths(hosts = []):
    for host in hosts: 
        paths = [default_paths[x] for x in default_paths if __salt__['mine.get'](x, 'inventory')[x]['fqdn'] == host][0]
        for path in paths: 
            result = add_folder(host, path)
    return True

def hosts_file_add(hostname):
    address = __salt__['mine.get']('fqdn:'+hostname,'address',expr_form='grain')
    address = address[address.keys()[0]][0]
    __salt__['file.append']('/etc/hosts',address+'\t'+hostname)

def add_host(hostname,script="None"):
	
	if not __salt__['file.file_exists']('/etc/backuppc/pc/'+hostname+'.pl'):
		hosts_file_add(hostname)
    		__salt__['file.touch']('/etc/backuppc/pc/'+hostname+'.pl')
    		__salt__['file.append']('/etc/backuppc/pc/'+hostname+'.pl', '$Conf{XferMethod} = \'rsync\';\n$Conf{RsyncShareName} = [\n];')
    		__salt__['file.chown']('/etc/backuppc/pc/'+hostname+'.pl', 'backuppc', 'www-data')
    		__salt__['file.append']('/etc/backuppc/hosts', hostname+'       0       backuppc')
        	__salt__['event.send']('backuppc/copykey', fqdn=hostname)
                __salt__['cmd.retcode'](cmd=rm_key+hostname, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
                __salt__['cmd.retcode'](cmd=sshcmd+hostname+' exit', runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
		if script != "None":
			__salt__['file.append']('/etc/backuppc/pc/'+hostname+'.pl','$Conf{DumpPreUserCmd} = \'$sshPath -q -x -l root $host '+script+'\';')
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
    __salt__['file.remove']('/etc/backuppc/pc/'+hostname+'.pl')
    __salt__['file.line'](path='/etc/backuppc/hosts',content=hostname+'       0       backuppc', mode='delete')
    __salt__['file.chown']('/etc/backuppc/hosts', 'backuppc', 'www-data')
    return __salt__['service.reload']('backuppc')

def add_folder(hostname, folder,script="None"):
        if not __salt__['file.file_exists']('/etc/backuppc/pc/'+hostname+'.pl'):
		add_host(hostname,script)
	if __salt__['file.search']('/etc/backuppc/pc/'+hostname+'.pl','\''+folder+'/?\''):
		return False
	elif __salt__['cmd.retcode'](cmd=sshcmd+hostname+' test ! -d '+folder, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc'):
		__salt__['file.replace']('/etc/backuppc/pc/'+hostname+'.pl', pattern="\$Conf\{RsyncShareName\} \= \[", repl="$Conf{RsyncShareName} = [\n  '"+folder+'\',')
		__salt__['service.reload']('backuppc')
		return True
	else:
		return False

def add_folder_list(hostname, folder_list,script="None"):
	for folder in folder_list:
		add_folder(hostname, folder,script)
 
def rm_folder(hostname, folder):
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
