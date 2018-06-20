import subprocess
import re
import datetime
import tempfile
import ldb
from .models import *


class SambaError(Exception):
    pass


class SambaProcessError(SambaError):
    def __init__(self, exc):
        exception_msg = 'Samba process returned %(rtn)i. Message: %(msg)s' % {
            'rtn': exc.returncode,
            'msg': exc.output
        }
        super(SambaProcessError, self).__init__(exception_msg)
        self.returncode = exc.returncode
        self.stdout = exc.output


def samba_tool(args):
    full_args = ['samba-tool'] + args
#    return subprocess.list2cmdline(full_args)
    return subprocess.check_output(full_args, stderr=subprocess.STDOUT)


def get_filter_from_username(username):
    return '(&(objectClass=user)(sAMAccountName=%s))' % ldb.binary_encode(username)


def get_user_by_username(username):
    try:
        return User.get(User.username == username)
    except User.DoesNotExist:
        return None

def get_group(group_name):
    try:
        return Group.get(Group.group_name == group_name)
    except Group.DoesNotExist:
        return None


def get_pdb_details(username):
    pdb_output = subprocess.check_output(['pdbedit', '-u ' + username,  # '-L',
                                          '-Lv'])
    parsed_out = {
        'username': unicode(re.search(r'Unix username: +(.*?)\n', pdb_output).group(1), errors = 'ignore'),
        'name': unicode(re.search(r'Full Name: +(.*?)\n', pdb_output).group(1), errors = 'ignore'),
        'flags': unicode(re.search(r'Account Flags: +\[(.*?)\]\n', pdb_output).group(1), errors = 'ignore').rstrip(),
        'password_expiry': unicode(re.search('Kickoff time: +(.*)\n', pdb_output).group(1), errors = 'ignore'), 
    }

    parsed_out['status'] = 'OK'
    if 'D' in parsed_out['flags'] : parsed_out['status'] = 'Disabled'
    if 'L' in parsed_out['flags']: 
        parsed_out['status'] = 'Locked'
        if 'D' in parsed_out['flags']: 
            parsed_out['status'] = 'Disabled, Locked'

    password_change_re = re.search(
        r"Password must change: [a-zA-Z]+, ([0-9]+ [a-zA-Z]+ [0-9]+)",
        pdb_output
    )
    if password_change_re is None:
        password_change = ''
    else:
        password_change = password_change_re.group(1)


#    try:
#        parsed_out['password_expiry'] = datetime.datetime.strptime(
#            password_change,
#            "%d %b %Y"
#        )
#    except ValueError:
#        parsed_out['password_expiry'] = None

    return parsed_out


def create_vpn_cert(username):
    def make_conf_from_template():
        with open('/vapour/data/openssl.tpl') as template_file:
            return template_file.read() % {
                'common_name': username
            }

    with tempfile.NamedTemporaryFile(delete=True) as conf_file:
        conf_str = make_conf_from_template()
        conf_file.write(conf_str)
        try:
            subprocess.check_output([
                    'openssl', 'req', '-batch', '-nodes',
                    '-new', '-newkey', 'rsa:2048',
                    '-keyout', '%s.key' % username,
                    '-out', '%s.csr' % username,
                    '-config', conf_file.name],
                cwd='/etc/openvpn/certificates/keys/')

            subprocess.check_output(
                [
                'openssl', 'ca',  '-batch', '-days', '3650', '-out', '%s.crt' %
                 username, '-in', '%s.csr' % username, '-config',
                 conf_file.name
                ], cwd='/etc/openvpn/certificates/keys/', stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            raise SambaProcessError(exc)
