import subprocess, re

def get_fileshares(path, extra_commands = []):
    command = ['du', path, '-d1', '-b'] + extra_commands
    result = subprocess.check_output(command).split('\n')
    result = [re.sub('\s+', ' ', x).split(' ') for x in result if x]
    result = [{'bytes' : x[0], 'folder' : x[1].split('/')[-1]} for x in result]
    return result

def get_all_fileshares():
    domain_command = ['grep', 'realm', '/etc/samba/smb.conf']
    domain = subprocess.check_output(domain_command).split(' = ')[1].strip()
    result = {'home' : get_fileshares('/home/', extra_commands = ['--exclude=/home/' + domain]), 'share' : get_fileshares('/home/' + domain + '/Share'), 'public' : get_fileshares('/home/' + domain + '/Public')}
    return result
