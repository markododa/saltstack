import salt

def add_host(hostname):
    __salt__['file.touch']('/etc/backuppc/pc/'+hostname+'.pl')
    __salt__['file.append']('/etc/backuppc/pc/'+hostname+'.pl', '$Conf{XferMethod} = \'rsync\';\n$Conf{RsyncShareName} = [\n];')
    __salt__['file.chown']('/etc/backuppc/pc/'+hostname+'.pl', 'backuppc', 'www-data')
    __salt__['file.append']('/etc/backuppc/hosts', hostname+'       0       backuppc')
    return True

def rm_host(hostname):
    __salt__['file.remove']('/etc/backuppc/pc/'+hostname+'.pl')
    __salt__['file.line'](path='/etc/backuppc/hosts',content=hostname+'       0       backuppc', mode='delete')
    __salt__['file.chown']('/etc/backuppc/hosts', 'backuppc', 'www-data')
    return __salt__['service.reload']('backuppc')

def add_folder(hostname, folder):
	sshcmd='ssh -oStrictHostKeyChecking=no root@'+hostname+' '
	if not __salt__['file.file_exists']('/etc/backuppc/pc/'+hostname+'.pl'):
		add_host(hostname)
        	__salt__['event.send']('backuppc/copykey', fqdn=hostname)
                __salt__['cmd.retcode'](cmd=sshcmd+'exit', runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc')
	if __salt__['file.search']('/etc/backuppc/pc/'+hostname+'.pl','\''+folder+'\','):
		return 'Folder is already put to be backuped up'
	elif __salt__['cmd.retcode'](cmd=sshcmd+'test ! -d '+folder, runas='backuppc', shell='/bin/bash',cwd='/var/lib/backuppc'):
		__salt__['file.replace']('/etc/backuppc/pc/'+hostname+'.pl', pattern="\$Conf\{RsyncShareName\} \= \[", repl="$Conf{RsyncShareName} = [\n  '"+folder+'\',')
	else:
		return 'Folder not found'
	__salt__['service.reload']('backuppc')
	return 'Folder has been added to backup'

def rm_folder(hostname, folder):
	if __salt__['file.line'](path='/etc/backuppc/pc/'+hostname+'.pl',content='\''+folder+'\',',mode='delete'):
		return 'Folder '+folder+' has been deleted from backup list'
	else:
		return 'Folder not in backup list'
        __salt__['file.chown']('/etc/backuppc/pc/'+hostname+'.pl', 'backuppc', 'www-data')
