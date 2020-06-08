import os,errno, subprocess
vcard_root = '/var/lib/vcards/'

vdirsync_config = """[general]
status_path = "~/.vdirsyncer/status/"

[pair {account_name}]
a = "{account_name}_folder"
b = "{account_name}_remote"
conflict_resolution = "b wins"
collections = ["from a", "from b"]

[storage {account_name}_folder]
type = "filesystem"
path = "{path}{account}/"
fileext = ".vcf"

[storage {account_name}_remote]
type = "carddav"
verify_fingerprint = "{fingerprint}"
verify = false

# We can simplify this URL here as well. In theory it shouldn't matter.
url = "https://{mx_host}/SOGo/dav/{account}/Contacts"
username = "{login_user}"
password = "{login_pass}"
"""

vcard = """BEGIN:VCARD
VERSION:3.0
UID:{uid}.vcf
CLASS:PUBLIC
PROFILE:VCARD
FN:{name}
EMAIL:{email}
END:VCARD
"""

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >= 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def create_vcard_config(account, config_update=False):
    account_name = account.split('@')[0]
    login_user = __salt__['pillar.get']('query_user')+'@'+__salt__['pillar.get']('domain')
    login_pass = __salt__['pillar.get']('query_password')
    fingerprint = __salt__['pillar.get']('va_email_https_fingerprint')
    mx_host = 'localhost'
    config_path=vcard_root+account+'/config'
    if not os.path.exists(config_path) or config_update==True:
        with open(config_path, 'w') as config_file:
            config_file.write(vdirsync_config.format(account=account, account_name=account_name, path=vcard_root, login_user=login_user, login_pass=login_pass, fingerprint=fingerprint, mx_host=mx_host))
            config_file.close()
            return True
    else:
        return "File unchanged"

def sync_vcards(account):
    subprocess.call(["vdirsyncer", "-c", vcard_root+account+'/config', "discover"])
    subprocess.check_output(["vdirsyncer", "-c", vcard_root+account+'/config', "sync", "--force-delete"])
    return True

def generate_vcard(account, recipient, name='', run_sync=True):
        path = vcard_root+account+'/personal/'
        if not os.path.exists(path):
            mkdir_p(path)
        if not os.path.exists(vcard_root+account+'/config'):
            create_vcard_config(account)
        with open(path+recipient+'.vcf', 'w') as vcf_file:
            vcf_file.write(vcard.format(uid=recipient,email=recipient, name=name))
            vcf_file.close()
        if run_sync:
            sync_vcards(account)
        return True

def generate_vcards(account, recipients):
    for recipient in recipients:
        generate_vcard(account, recipient["address"], name=recipient["name"],run_sync=False)
    return sync_vcards(account)

def remove_vcard(account, recipient):
    path = vcard_root+account+'/personal/'
    os.remove(path+recipient+'.vcf')
    return sync_vcards(account)

def get_vcard(account, recipient):
    path = vcard_root+account+'/personal/'
    with open(path+recipient+'.vcf', 'r') as vcf_file:
        #return { x.split(":")[0]:x.split(":")[1] for x in vcf_file.read().split('\n') if ':' in x}
        return dict( l.split(":") for l in vcf_file.read().split('\n') if ':' in l)
