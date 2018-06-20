import samba
from samba.dcerpc import security, dnsserver
import ldb
import subprocess
import re
import datetime
import json
import samba_parser
from samba.credentials import Credentials, DONT_USE_KERBEROS
from samba.auth import system_session
from samba.netcmd.common import netcmd_get_domain_infos_via_cldap
from samba.samdb import SamDB
from ldb import SCOPE_SUBTREE, SCOPE_BASE
from samba import param, dsdb
from samba.provision import ProvisionNames, provision_paths_from_lp
from samba.param import LoadParm

__version__ = '0.0.5'

lp = LoadParm()
lp.load_default()
smbconf = lp.configfile
creds = Credentials()
creds.guess(lp)
session = system_session()
def get_paths():
    smbconf = param.default_path()
    lp = param.LoadParm()
    lp.load(smbconf)
    return provision_paths_from_lp(lp, 'foo')
paths = get_paths()
sam_ldb = SamDB(url=paths.samdb, session_info=session, credentials=creds, lp=lp)

dash_args = ['last_name', 'description', 'phone', 'first_name', 'display_name', 'company', 'email', 'axi_enabled', 'physical_delivery_office_name', 'mobile', 'profile_path', 'script_path', 'home_phone', 'axi_is_enabled']
api_args = ['sn', 'description', 'telephoneNumber', 'givenName', 'displayName', 'company', 'mail', 'axiIsEnabled', 'physicalDeliveryOfficeName', 'mobile', 'profilePath', 'scriptPath', 'homePhone', 'axiIsEnabled']



#TODO
#Remove all usage of the cache. 
#In order to keep a sane enough speed, we will use proper ldap searches. 
#So far, these are only two functions which use the cache: list_users and get_groups.
#We will also need to rewrite some other functions. 

#In the end, we will have these: 
#list_users() - ldbsearch -a -H ldap://127.0.0.1 -Uvadmin%Qwert~12 '(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=elem,DC=com,DC=mk)' dn sAMAccountName name description userAccountControl
#get_groups() - ldbsearch -a -H ldap://127.0.0.1 -Uvadmin%Qwert~12 '(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=elem,DC=com,DC=mk)' dn sAMAccountName name description 
#get_groups_for_user() - ldbsearch -a -H ldap://127.0.0.1 -Uvadmin%Qwert~12 '(CN=sasko stojanovski)' memberOf
#get_users_for_group() - already exists
#get_user_groups() - ldbsearch -a -H ldap://127.0.0.1 -Uvadmin%Qwert~12 '(CN=sasko stojanovski)' memberOf


def samba_tool(cmd): 
    return subprocess.check_output(['samba-tool'] + cmd)

def get_filter_from_username(username):
    return '(&(objectClass=user)(sAMAccountName=%s))' % ldb.binary_encode(username)


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

    return parsed_out


def element_to_dict(e):
    e = e.split(',')
    e = [x.split('=') for x in e]
    e = [(x[0], [i[1] for i in e if i[0] == x[0]]) for x in e]
    e = dict(e)
    return e

def call_samdb_function(func, kwargs):
    getattr(sam_ldb, func)(**kwargs)

def get_cur_domain():
    """Returns the domain name of the local Samba directory."""
    res = netcmd_get_domain_infos_via_cldap(lp, None, '127.0.0.1')
    return res.dns_domain

def users_last_logins():
    return samba_parser.open_and_parse_log('/var/log/lastlogin.log')

def users_log():
    return samba_parser.open_and_parse_log('/var/log/user.log')


def get_group_dn(ldb_instance, group_name):
    search_filter = '(&(objectclass=group)(cn=%s))' % group_name
    print 'Search is : ', search_filter
    return get_object_dn(ldb_instance, group_name, search_filter, ['cn'])

def get_user_dn(ldb_instance, username):
    search_filter = get_filter_from_username(username)
    return get_object_dn(ldb_instance, username, search_filter,  ['userAccountControl'])

def get_object_dn(ldb_instance, object_name, search_filter, attrs):
    res = ldb_instance.search(
        base=str(ldb_instance.get_default_basedn()),
        scope=ldb.SCOPE_SUBTREE,
        expression=search_filter, attrs=attrs
    )

    return res.msgs[0].dn

def list_to_ldap_mod(d): 
    mod = '\n' + '\n'.join(['%s: %s' % (x[0], x[1]) for x in d])
    return mod


def change_attr(name, attr, new_value, object_type = 'user'):
    if not new_value: 
        return handle_attr(name, attr, new_value, object_type, action = 'delete')
    handle_attr(name, attr, new_value, object_type, action = 'replace')

def add_attr(name, attr, new_value, object_type = 'user'):
    handle_attr(name, attr, new_value, object_type, action = 'add')

def handle_attr(name, attr, new_value, object_type = 'user', action = 'replace'):
    object_dn = {
        'user' : get_user_dn, 
        'group' : get_group_dn
    }[object_type](sam_ldb, name)

    ldap_mod = [
        ('dn', object_dn), 
        ('changetype', 'modify'), 
        (action, attr), 
    ] 
    if action != 'delete' : 
        ldap_mod.append((attr, new_value))
    mod = list_to_ldap_mod(ldap_mod)
    print ('mod is : ', mod)
    sam_ldb.modify_ldif(mod)



def get_user_data(username):
    user_dn = get_user_dn(sam_ldb, username)

    domain_dn = sam_ldb.domain_dn()

    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression=(str(user_dn).split(',')[0]), attrs=['*']).msgs or [{}]
    res = res[0]
    user = dict(res)

    dash_args = ['last_name', 'description', 'phone', 'first_name', 'display_name', 'company', 'email', 'axi_is_enabled', 'physical_delivery_office_name', 'mobile', 'profile_path', 'script_path', 'home_phone', ]
    api_args = ['sn', 'description', 'telephoneNumber', 'givenName', 'displayName', 'company', 'mail', 'axiIsEnabled', 'physicalDeliveryOfficeName', 'mobile', 'profilePath', 'scriptPath', 'homePhone', ]
    user = {x[0] : user.get(x[1])[0] if user.get(x[1]) else '' for x in zip(dash_args, api_args)}
    return user



#kwargs added for compatibility, not actually used. 
def list_users(skip_groups = False, skip_samba_log = False):
    """Returns a list of all users (and their pdb data)"""
    domain_dn = sam_ldb.domain_dn()
    result = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression='(objectCategory=CN=Person,CN=Schema,CN=Configuration,%s)' % domain_dn, attrs=['dn', 'sAMAccountName', 'name', 'description', 'userAccountControl']).msgs or [{}]
    users = [{
        'username' : user.get('sAMAccountName')[0],
        'name' : user.get('name')[0], 
        'ctl' : user.get('userAccountControl')[0],
        'password_expiry' : "",
        'last_logon' : "",
        'status' : "OK",
        'ip_address' : "",
        'computer' : ""
    } for user in result]

    args_defaults = [('description', '')]
    for user in zip(users, result): 
        extra_args = {}
        for arg in args_defaults: 
            val = user[1].get(arg[0]) or [arg[1]]
            val = val[0]
            user[0][arg[0]] = val

    samba_flags = {
        -4 : 'Locked', 
        -2 : 'Disabled',
    }


    samba_log = users_last_logins()

    for u in users: 
        user_bits = bin(int(u['ctl']))[2:]
        user_flags = ''
        for flag in samba_flags : 
            if user_bits[flag] == '1': 
                user_flags += samba_flags[flag] + ', '
        u['flags'] = user_flags[:-2]
        
        user_log = [x for x in samba_log if x['info']['username'] == u['username']] or [{}]
        user_log = user_log[-1]
        if user_log: 
            u['ip_address'] = user_log['info']['address']
            u['computer'] = user_log['info']['computer']
            u['last_login'] = user_log['date']

#    groups = get_groups_with_users()
    groups = []
    result = {'users' : users, 'users_log': samba_log, 'groups' : groups}



    return result

def delete_user(username):
    sam_ldb.deleteuser(username)


def change_name(username, new_name):
    """Finds a Samba user by username and then sets it's full name"""
    try:
        subprocess.check_output(['pdbedit', '-u' + username, '-f' + new_name],
                                stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        raise SambaProcessError(exc)


def edit_user(username, new_user_data):

    old_user_data = get_user_data(username)
    api_args = ['sn', 'description', 'telephoneNumber', 'givenName', 'displayName', 'company', 'mail', 'axiIsEnabled', 'physicalDeliveryOfficeName', 'mobile', 'profilePath', 'scriptPath', 'homePhone', ]
    dash_args = ['last_name', 'description', 'phone', 'first_name', 'display_name', 'company', 'email', 'axi_is_enabled', 'physical_delivery_office_name', 'mobile', 'profile_path', 'script_path', 'home_phone', ]


    for attr in dash_args: 
         if not new_user_data.get(attr):
             continue
         if old_user_data.get(attr) != new_user_data[attr]:
             if attr not in api_args: 
                 attr_key = api_args[dash_args.index(attr)]
             else: attr_key = attr
             val = new_user_data[attr]
             if isinstance(val, bool):
                 val = ('TRUE' if val else 'FALSE')
             else:
                 val = str(val)
             change_attr(username, attr_key, val)

def add_user(username, password, name, surname, email, organizational_unit = None, change_at_next_login = False, attrs = {}):
    """Adds a new user to Samba and then puts it into cache"""

    organizational_unit = ['--userou', 'OU=' + organizational_unit] if organizational_unit else []
    change_pass = ['--must-change-at-next-login'] if change_at_next_login else []
    name = ['--given-name', name] if name else []
    surname = ['--surname', surname] if surname else []
    email = ['--mail-address', email] if email else []


#        sam_ldb.newuser(username = username, password = password, surname = surname, givenname = name, mailaddress = email, useusernameascn = False, userou = 'OU=' + organizational_unit)
    # Using the SamDB api is weird because it sets the display name to be givenname.surname, instead of the proper display name. This is why we (temporarily?) use samba_tool. 

    samba_args = ['user', 'add', username, password] + name + surname + email + organizational_unit + change_pass
    result = samba_tool(samba_args)
    user_data = get_pdb_details(username)
#        raise SambaProcessError(exc)

    edit_user(username, attrs)

def change_password(username, password, again_at_login=False):
    sam_filter = get_filter_from_username(username)
    sam_ldb.setpassword(sam_filter, password, force_change_at_next_login=again_at_login, username=username)
    try:
        user_data = get_pdb_details(username)
        # After updating Samba, update password expiry date in the cache
    except subprocess.CalledProcessError:
        raise SambaProcessError(exc)


def list_dns():
    from samba.dcerpc import dnsp, dnsserver
    server = '127.0.0.1'
    binding_str = 'ncacn_ip_tcp:%s[sign]' % server

    cred_data = open('/vapour/dnsquery').read().split(':')

    creds = Credentials()
    creds.guess(lp)
    creds.set_username(cred_data[0])
    creds.set_password(cred_data[1].rstrip())
    dns_conn = dnsserver.dnsserver(binding_str, lp, creds)
    zone = get_cur_domain()
    name = '@'
    record_type = dnsp.DNS_TYPE_ALL
    select_flags = dnsserver.DNS_RPC_VIEW_AUTHORITY_DATA
    
    buflen, res = dns_conn.DnssrvEnumRecords2(
            dnsserver.DNS_CLIENT_VERSION_LONGHORN, 0, server, zone, name,
            None, record_type, select_flags, None, None
    )
    record_groups = res.rec
    result = []
    for rec_group in record_groups:
        group_name = rec_group.dnsNodeName.str
        for rec in rec_group.records:
            if rec.wType == dnsp.DNS_TYPE_A:
                result.append({'group_name': group_name, 'type': 'A', 'value': rec.data})
            elif rec.wType == dnsp.DNS_TYPE_AAAA:
                result.append({'group_name': group_name, 'type': 'AAAA', 'value': rec.data})
            elif rec.wType == dnsp.DNS_TYPE_PTR:
                result.append({'group_name': group_name, 'type': 'PTR', 'value': rec.data.str})
            elif rec.wType == dnsp.DNS_TYPE_NS:
                result.append({'group_name': group_name, 'type': 'NS', 'value': rec.data.str})
            elif rec.wType == dnsp.DNS_TYPE_CNAME:
                result.append({'group_name': group_name, 'type': 'CNAME', 'value': rec.data.str})
            elif rec.wType == dnsp.DNS_TYPE_SOA:
                result.append({
                    'group_name': group_name,
                    'type': 'SOA',
                    'value': 'serial=%d, refresh=%d, retry=%d, expire=%d, minttl=%d, ns=%s, email=%s' % (
                        rec.data.dwSerialNo,
                        rec.data.dwRefresh,
                        rec.data.dwRetry,
                        rec.data.dwExpire,
                        rec.data.dwMinimumTtl,
                        rec.data.NamePrimaryServer.str,
                        rec.data.ZoneAdministratorEmail.str
                    )
                })
            elif rec.wType == dnsp.DNS_TYPE_MX:
                result.append({'group_name': group_name, 'type': 'MX', 'value': '%s (%d)' % (rec.data.nameExchange.str, rec.data.wPreference)})
            elif rec.wType == dnsp.DNS_TYPE_SRV:
                result.append({'group_name': group_name, 'type': 'SRV', 'value': '%s (%d, %d, %d)' % (
                    rec.data.nameTarget, rec.data.wPort,
                    rec.data.wPriority, rec.data.wWeight
                )})
            elif rec.wType == dnsp.DNS_TYPE_TXT:
                slist = ['"%s"' % name.str for name in rec.data]
                result.append({'group_name': group_name, 'type': 'TXT', 'value': ','.join(slist)})
    return result

def add_dns(name, entry_type, data):
    return manage_dns_entry(name, entry_type, data, 'add')

def delete_dns(name, entry_type, data):
    return manage_dns_entry(name, entry_type, data, 'delete')

def add_dns(name, entry_type, data):
    return manage_dns_entry(name, entry_type, data, 'add')

def delete_dns(name, entry_type, data):
    return manage_dns_entry(name, entry_type, data, 'delete')

def manage_dns_entry(name, entry_type, data, action):
#    try:
    cred_data = open('/vapour/dnsquery').read().rstrip().replace(':', '%')
    args = []
    if entry_type in ['A', 'AAAA']:
        args = ["dns", action, "localhost", get_cur_domain(), name, entry_type, data['address']]
    elif entry_type == 'MX':
        if not name : name = '@'
        if not '.' in data['hostname'] : data['hostname'] += '.' + get_cur_domain()
        args = ["dns", action, "localhost", get_cur_domain(), name, entry_type, data['hostname'] + ' ' + data['priority']]
    elif entry_type in ['NS', 'CNAME']:
        if not name : name = '@'
        if not '.' in data['hostname'] : data['hostname'] += '.' + get_cur_domain()
        args = ["dns", action, "localhost", get_cur_domain(), name, entry_type, data['hostname']]
    result = samba_tool(args + ['-U', cred_data])
#    except subprocess.CalledProcessError as exc:
#        raise SambaProcessError(exc)

def update_dns_entry(name, entry_type, old_data, new_data):
#    try:
    cred_data = open('/vapour/dnsquery').read().rstrip().replace(':', '%')
    args = ['dns', 'update', 'localhost', get_cur_domain(), name, entry_type]
    if entry_type in ['A', 'AAAA']:
        args += [old_data['address'], new_data['address']]
    elif entry_type in ['NS', 'CNAME']:
        args += [old_data['hostname'], new_data['hostname']]
    elif entry_type == 'MX':
        args += [old_data['hostname'] + ' ' + old_data['priority'], new_data['hostname'] + ' ' + new_data['priority']]
    return samba_tool(args + ['-U', cred_data])
#    except subprocess.CalledProcessError as exc:
#        raise SambaProcessError(exc)


def get_ou_members(ou_name):
    domain_dn = sam_ldb.domain_dn()
    
    res_ous = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression=("(objectClass=organizationalUnit)"), attrs=[])
    ou = [x.get('dn') for x in res_ous if x.get('dn').get_component_value(0) == ou_name] or [None]
    ou = ou[0]
    if not ou: 
        return []
    res_people = sam_ldb.search(base = ou.get_linearized(), scope=ldb.SCOPE_SUBTREE, expression=("(objectClass=person)"), attrs=['samaccountname']).msgs

    if len(res_people) == 0: 
        return []

    res = [x.get('sAMAccountName')[0] for x in res_people]
    return res


def create_organizational_unit(name, description):
    ou_dn = 'OU=%s,' % (name) + get_dc()
    sam_ldb.create_ou(ou_dn = ou_dn, name = name, description = description)

def list_organizational_units():
    domain_dn = sam_ldb.domain_dn()
    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression=("(objectClass=organizationalUnit)"), attrs=['ou', 'description'])

    if len(res) == 0: 
        return []
    ous = [[str(x.get('ou')), str(x.get('description'))] for x in res]

    return ous

def change_ou(username, ou_name = None):
    user_dn = str(get_user_dn(sam_ldb, username))
    user_cn = user_dn.split(',')[0]

    if ou_name:
        ou_dn = 'OU=%s,' % (ou_name) + get_dc()
    else: 
        ou_dn = 'CN=Users,' + get_dc()

    mod = [('dn', user_dn), ('changetype', 'modrdn'), ('newrdn', user_cn), ('deleteoldrdn', '1'), ('newsuperior', ou_dn)]
    mod = list_to_ldap_mod(mod)


    file_path = '/tmp/change_ou_%s.ldif' % username

    with open(file_path, 'w') as f: 
        f.write(mod)

    cred_data = open('/vapour/dnsquery').read().split(':')

    cred_filter = get_filter_from_username(cred_data[0])
    cred_dn = str(get_user_dn(sam_ldb, cred_data[0]))


    #Using a file with ldapmodify because for some reason, modify_ldif does not work properly. 
    mod_cmd = ['ldapmodify', '-D', cred_dn, '-w', cred_data[1].rstrip('\n'), '-f', file_path]
    result = subprocess.check_output(mod_cmd)


#    sam_ldb.modify_ldif(mod)


def edit_group_attrs(name, attrs):
    for attr in attrs: 
        change_attr(name, attr, attrs[attr], object_type = 'group')


def get_groups():
    domain_dn = sam_ldb.domain_dn()
    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE,
                       expression=("(objectClass=group)"),
                       attrs=["samaccountname", "description", "mail", "grouptype"])
    if len(res) == 0:
        return
    else:
        return [[msg.get("samaccountname", idx=0), msg.get('mail', idx = 0), msg.get('description', idx = 0)] for msg in res]

def get_groups_with_users():
    domain_dn = sam_ldb.domain_dn()
    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE,
                       expression=("(objectClass=group)"),
                       attrs=["samaccountname", "member"])
    if len(res) == 0:
        return
    else:
        res = [x for x in res][:3]
        return { msg.get("samaccountname")[0] : [element_to_dict(x)['CN'][0] for x in msg.get('member', [])]  for msg in res}


def delete_group(group_name):
    result = samba_tool(['group', 'delete', group_name])

def add_group(name, attrs = {}):
    sam_ldb.newgroup(name)
    edit_group_attrs(name, attrs)

def list_group_members(group):
    members = samba_tool(['group', 'listmembers', group])
    members = members.rstrip('\n').split('\n')
    members = [x for x in members if x]
    return members

def get_user_groups(username):
    domain_dn = sam_ldb.domain_dn()
    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression=("(CN=%s)" % username),  attrs=["memberOf"])
    res = [element_to_dict(x)['CN'][0] for x in res.msgs[0].get('memberOf')]
    groups_names = []
    for cn in res: 
        group = sam_ldb.search(domain_dn, scope=ldb.SCOPE_SUBTREE, expression=("(CN=%s)" % (cn)),  attrs=["samaccountname"])
        group_name = group.msgs[0].get('sAMAccountName')[0]
        groups_names.append(group_name)
    return groups_names

def manage_user_groups(username, groups, action = 'addmembers'):
    for group in groups:
        try:
            samba_tool(['group', action, group, username])
        except Exception:
            return False
    return True

def update_user_groups(user, add_to_groups, remove_from_groups):
    all_users = list_users()

    user = [x for x in all_users['users'] if x['username'] == user or x['name'] == user] or [None]
    user = user[0]

    if not user: return False
    user = user['username']
    if not manage_user_groups(user, add_to_groups): return False
    if manage_user_groups(user, remove_from_groups, 'removemembers'): return True

#Argument is a dictionary of form {'username':['group1', 'group2'...], ...}
def manage_users_in_groups(users_groups, action = 'addmembers'):
    for user in users_groups:
        try :
            manage_user_groups(user, users_groups[user], action)
        except Exception:
            return False
    return True

def unlock_user(username): 
    user_data = get_pdb_details(username)
    flags = ''.join([c for c in user_data['flags'] if c != 'L'])
    
    pdb_cmd = ['pdbedit', "-c='[%s]'"%flags, username]
    subprocess.check_output(pdb_cmd)

def set_user_status(username, status):
    """Locks or unlocks a specific user."""
    sam_filter = get_filter_from_username(username)
    func = {
        'disable': sam_ldb.disable_account,
        'enable': sam_ldb.enable_account 
    }
    func[status](sam_filter)
    user_data = get_pdb_details(username)

def disable_user(username):
    return set_user_status(username, 'disable')

def enable_user(username):
    return set_user_status(username, 'enable')

def add_alias(username, alias):
    user_dn = get_user_dn(sam_ldb, username)
    mod = '\n' + 'dn: %s' % user_dn + '\n' + \
          'changetype: modify' + '\n' + \
          'add: proxyAddresses' + '\n' + \
          'proxyAddresses: SMTP:%s' % alias + '\n'
    sam_ldb.modify_ldif(mod)
    

def get_dc_info():
    res = netcmd_get_domain_infos_via_cldap(lp, None, '127.0.0.1')
    return {'forest' : res.forest, 'domain' : res.dns_domain, 'domain_name': res.domain_name, 'pdc_dns_name' : res.pdc_dns_name, 'pdc_name' : res.pdc_name, 'server_site' : res.server_site, 'client_site' : res.client_site}
    
    
def level_show():
    domain_dn = sam_ldb.domain_dn()

    res_forest = sam_ldb.search("CN=Partitions,%s" % sam_ldb.get_config_basedn(), scope=ldb.SCOPE_BASE, attrs=["msDS-Behavior-Version"])[0]['dn']
    assert len(res_forest) == 1

    res_domain = sam_ldb.search(domain_dn, scope=ldb.SCOPE_BASE, attrs=["msDS-Behavior-Version", "nTMixedDomain"])[0]['dn']
    assert len(res_domain) == 1

    res_dc_s = sam_ldb.search("CN=Sites,%s" % sam_ldb.get_config_basedn(), scope=ldb.SCOPE_SUBTREE, expression="(objectClass=nTDSDSA)",    attrs=["msDS-Behavior-Version"])[0]['dn']
    assert len(res_dc_s) >= 1 
    
    return {'forest' : str(res_forest), 'domain' : str(res_domain), 'dc_s' : str(res_dc_s)}
   

def fsmo_show():
    domain_dn = sam_ldb.domain_dn()
    
    fsmo_args = { 'infrastructure_dn' : "CN=Infrastructure," + domain_dn, 'naming_dn' : "CN=Partitions,%s" % sam_ldb.get_config_basedn(), 'schema_dn' : sam_ldb.get_schema_basedn(), 'rid_dn' : "CN=RID Manager$,CN=System," + domain_dn}
    
    res = {}
    
    for attr in fsmo_args:
        temp_res = sam_ldb.search(fsmo_args[attr], scope = ldb.SCOPE_BASE, attrs = ['fsmoRoleOwner'])
        assert len(temp_res) == 1
        res[attr] = temp_res[0]['fsmoRoleOwner'][0]
        
    return res
        
    

def get_dc():
    domain = get_cur_domain()
    dc = 'DC=' +domain.replace('.', ',DC=')
    return dc
    
def get_passwordsettings():
    domain_dn = sam_ldb.domain_dn()
    res = sam_ldb.search(domain_dn, scope=ldb.SCOPE_BASE, attrs=["pwdProperties", "pwdHistoryLength", "minPwdLength", "minPwdAge", "maxPwdAge", "lockoutDuration", "lockoutThreshold", "lockOutObservationWindow"])[0]
    return {x: str(res[x]) for x in res}
    
def get_gpo():
    policies_dn = sam_ldb.get_default_basedn()
    policies_dn.add_child(ldb.Dn(sam_ldb, "CN=Policies,CN=System"))

    base_dn = policies_dn
    search_expr = "(objectClass=groupPolicyContainer)"
    search_scope = ldb.SCOPE_ONELEVEL

    sd_flags=security.SECINFO_OWNER|security.SECINFO_GROUP|security.SECINFO_DACL|security.SECINFO_SACL
    
    res = list(sam_ldb.search(base=base_dn, scope=search_scope, expression=search_expr, attrs=['versionNumber', 'flags', 'name', 'displayName'], controls=['sd_flags:1:%d' % sd_flags]))
    return [{i : str(x[i]) for i in x} for x in res]
    return {x: str(res[x]) for x in res if x != 'nTSecurityDescriptor'}


def get_dns_zones():
    request_filter = dnsserver.DNS_ZONE_REQUEST_PRIMARY
    server = '127.0.0.1'
    binding_str = 'ncacn_ip_tcp:%s[sign]' % server
    cred_data = open('/vapour/dnsquery').read().split(':')

    creds = Credentials()
    creds.guess(lp)
    creds.set_username(cred_data[0])
    creds.set_password(cred_data[1].rstrip())

    dns_conn = dnsserver.dnsserver(binding_str, lp, creds)
    client_version = dnsserver.DNS_CLIENT_VERSION_LONGHORN

    typeid, res = dns_conn.DnssrvComplexOperation2(client_version, 0, server, None, 'EnumZones', dnsserver.DNSSRV_TYPEID_DWORD, request_filter)

    return dict(res)

def output_to_dict(samba_output):
    samba_output = samba_output.split('\n\n')
    outputs = []
    for output in samba_output: 
        output = [x for x in output.split('\n') if ':' in x]
        output =  dict([x.split(':') for x in output if x])
        output = {x.strip() : output[x].strip() for x in output}
        if output: 
            outputs.append(output)

    if len(outputs) == 1: 
        outputs = outputs[0]

    return outputs

def get_overview_info():

    #All of these functions for getting samba values do work, the only problem being that they return values not in a human friendly way and need a lot of code just for proper text parsing. 
    #Performance is a non-issue here, since we're only executing 5 commands. Using module functions will only probably save a few milliseconds at the cost of a lot more keystrokes. 
#    schema = level_show()
#    roles = fsmo_show()
#    pass_settings = get_passwordsettings()
#    list_gpos = get_gpo()
#    dns_zones = get_dns_zones()
#    dc_info = get_dc_info()

    dc_info = output_to_dict(samba_tool(['domain', 'info', '127.0.0.1']))
    schema = output_to_dict(samba_tool(['domain', 'level', 'show']))
    roles = output_to_dict(samba_tool(['fsmo', 'show']))
    pass_settings = output_to_dict(samba_tool(['domain', 'passwordsettings', 'show']))
    list_gpos = output_to_dict(samba_tool(['gpo', 'listall']))
    #dns_zones currently not used
    dns_zones = {}
    joined_computers = [x.split(':')[0] for x in subprocess.check_output(['pdbedit', '-L']) if '$' in x]

    overview_info = {'dc_info' : dc_info, 'schema' : schema, 'roles' : roles, 'pass_settings' : pass_settings, 'list_gpos' : list_gpos, 'dns_zones' : dns_zones, 'joined_computers' : joined_computers}

    return overview_info

