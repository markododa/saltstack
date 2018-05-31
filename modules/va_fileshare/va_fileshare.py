import subprocess, va_utils, json, re
from va_utils import check_functionality as panel_check_functionality
from va_fileshare_panels import panels


def get_fileshares(path, share_type, extra_commands = []):
    command = ['du', path, '-d1', '-b', '-m'] + extra_commands
    result = subprocess.check_output(command).split('\n')
    result = [re.sub(r'\s+', ' ', x).split(' ') for x in result if x]
    result = [{'share' : share_type, 'path': path+x[1].split('/')[-1], 'size' : int(x[0]), 'subfolder' : x[1].split('/')[-1]} for x in result]
    result = sorted(result, key = lambda x: x['size'], reverse = False)
#content = sorted(content, key = lambda x: x['startTime'], reverse = True)   
    return result
#[{'host' : x, 'total_backups': backupTotals(x), 'protocol' : get_host_protocol(x)} for x in host_list]

def panel_all_fileshares():
    domain_command = ['grep', 'realm', '/etc/samba/smb.conf']
    domain = subprocess.check_output(domain_command).split(' = ')[1].strip().lower()

    home_shares =   get_fileshares('/home/', share_type = 'Personal', extra_commands = ['--exclude=/home/' + domain])
    public_shares = get_fileshares('/home/' + domain + '/Public/', share_type = 'Public')
    other_shares =  get_fileshares('/home/' + domain + '/Share/', share_type = 'Share')

    result = home_shares + public_shares + other_shares
    return result

def panel_statistics():
    diskusage =__salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /home/ -o TARGET').split()[1]]
    statistics = [{'key' : 'Shares partition used size (MB)', 'value': int(diskusage['used'])/1024},
                {'key' : 'Shares partition free space (MB)', 'value': int(diskusage['available'])/1024},
                {'key' : 'Shares partition mount point', 'value': diskusage['filesystem']}]
    return statistics
