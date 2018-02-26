# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
import va_samba_api
import json
from va_utils import check_functionality as panel_check_functionality
from va_directory_panels import panels


#import samba_parser

builtin_groups = ['Domain Controllers','Domain Guests', 'Guests', 'Domain Computers', 'Account Operators', 'Group Policy Creator Owners', '' 'DnsAdmins','Enterprise Admins','Backup Operators','Allowed RODC Password Replication Group','Cert Publishers','Certificate Service DCOM Access','Cryptographic Operators','Denied RODC Password Replication Group','Distributed COM Users','DnsUpdateProxy','Enterprise Read-Only Domain Controllers','Event Log Readers', 'IIS_IUSRS', 'Incoming Forest Trust Builders','Network Configuration Operators','Performance Log Users', 'Performance Monitor Users','Pre-Windows 2000 Compatible Access','Print Operators','RAS and IAS Servers','Read-Only Domain Controllers','Replicator','Schema Admins', 'Server Operators', 'Terminal Server License Servers', 'Windows Authorization Access Group']
panel_list_dns = list_dns

def panel_ou_members(ou_name):
    ou_members = get_ou_members(ou_name)
    ou_source = [{'member' : x,"type":' - '} for x in ou_members]
    #ou_source = [{'member' : x[0],"type":', '.join(x[1])} for x in ou_members]
    #NINO ne go vraka tipot, samo first name?
    return ou_source

def format_dns_arguments(entry_type, entry_data):
    if entry_type in ['A', 'AAAA']:
        entry_data = {'address' : entry_data}
    elif entry_type == 'MX':
        if " " in entry_data: 
            #must strip () from priority when removing the record
            entry_data = {'hostname' : entry_data.split(' ')[0], 'priority' : entry_data.split(' ')[1].replace('(','').replace(')','')}
        else:
            #default pririty 10 if not entered
            entry_data = {'hostname' : entry_data.split(' ')[0], 'priority' : '10'} 
    elif entry_type in ['NS', 'CNAME']:
        entry_data = {'hostname' : entry_data}

    return entry_data

def action_edit_dns(entry_name, entry_type, old_data, new_data = {}):
    old_data = format_dns_arguments(entry_type, old_data)

    new_data = format_dns_arguments(entry_type, new_data)
    if (entry_name==''):
        entry_name=get_cur_domain()
    return update_dns_entry(entry_name, entry_type, old_data, new_data)

def action_add_dns(entry_type, entry_name, entry_data):
    entry_data = format_dns_arguments(entry_type,entry_data)
    return add_dns(entry_name, entry_type, entry_data) 

def action_rm_dns(entry_name, entry_type, entry_data):
    entry_data = format_dns_arguments(entry_type,entry_data)
    return delete_dns(entry_name, entry_type, entry_data)

def panel_manage_groups(user_name):
    group_memberships = get_user_groups(user_name)
    membership_source = [{'groupname' : x} for x in group_memberships]
    return membership_source

def panel_list_group_members(group_name):
    group_members = list_group_members(group_name)
    group_source = [{'username' : x} for x in group_members]
    return group_source

def panel_list_users():
    return list_users()['users']

def action_add_group(name, description, mail):
    attrs = {'description':description, 'mail': mail}
    result = add_group(name, attrs)
    return result

def panel_get_groups():
    groups = get_groups()
    groups = [{"groupname" : x[0], "description" : x[2], "email" : x[1]} for x in groups]
    return groups

def panel_get_groups_builtin():
    groups = get_groups()
    filtered_groups=[]
    for group in groups:
        if group[0] in builtin_groups:
            filtered_groups.append({"groupname" : group[0], "description" : group[2], "email" : group[1]})
    return filtered_groups

def panel_get_groups_handmade():
    groups = get_groups()
    filtered_groups=[]
    for group in groups:
        if group[0] not in builtin_groups:
            filtered_groups.append({"groupname" : group[0], "description" : group[2], "email" : group[1]})
    return filtered_groups

def panel_list_organizational_units():
    org_units = list_organizational_units()
    org_units = [{'name' : x[0], 'description' : x[1]} for x in org_units]
    return org_units

def panel_get_pass_settings():
    pass_settings = output_to_dict(samba_tool(['domain', 'passwordsettings', 'show']).split('\n')[1:])
    pass_settings = [{'key' : x, 'value'  : pass_settings[x]} for x in pass_settings]
    return pass_settings

def panel_level_show():
    res = output_to_dict(samba_tool(['domain', 'level', 'show']).split('\n')[1:])
    res = [{'key' : x, 'value'  : res[x]} for x in res]
    return res

def panel_get_pcs():
    res = samba_tool(['group', 'listmembers','Domain Computers']).split('\n')
    res = [{'hostname' : x.replace('$','')} for x in res if x]
    return res

def panel_get_dcs():
    res = samba_tool(['group', 'listmembers','Domain Controllers']).split('\n')
    res = [{'hostname' : x.replace('$','')} for x in res if x]
    return res

def panel_get_dc_info():
    res = netcmd_get_domain_infos_via_cldap(lp, None, '127.0.0.1')
    res = {'forest' : res.forest, 'domain' : res.dns_domain, 'domain_name': res.domain_name, 'pdc_dns_name' : res.pdc_dns_name, 'pdc_name' : res.pdc_name, 'server_site' : res.server_site, 'client_site' : res.client_site}
   
    #pass_settings = output_to_dict(samba_tool(['domain', 'passwordsettings', 'show']).split('\n')[1:])
    res = [{'key' : x.replace('_',' ').title(), 'value'  : res[x]} for x in res]
    return res

def panel_gpo_polices():
    res = output_to_dict(samba_tool(['gpo', 'listall']).split('\n'))
    res['gpo'] = res.pop('GPO')
    return [res]

def panel_fsmo_show():
    res = samba_tool(['fsmo', 'show']).split('\n')
    res = [{'key' : x.split(' owner: ')[0].replace('MasterRole',''), 'value': x.split(' owner: ')[1].replace('CN=NTDS Settings,CN=','').split(',CN=Servers,')[0]} for x in res if x]
    #CN=NTDS Settings,CN=VA-DIRECTORY,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=domain,DC=com
    return res


def panel_fsmo_show_old():
    domain_dn = sam_ldb.domain_dn()

    fsmo_args = { 'infrastructure_dn' : "CN=Infrastructure," + domain_dn, 'naming_dn' : "CN=Partitions,%s" % sam_ldb.get_config_basedn(), 'schema_dn' : sam_ldb.get_schema_basedn(), 'rid_dn' : "CN=RID Manager$,CN=System," + domain_dn}

    res = {}

    for attr in fsmo_args:
        temp_res = sam_ldb.search(fsmo_args[attr], scope = ldb.SCOPE_BASE, attrs = ['fsmoRoleOwner'])
        assert len(temp_res) == 1
        res[attr] = temp_res[0]['fsmoRoleOwner'][0]
    res = [{'key' : x.replace('_dn','').title(), 'value'  : res[x].split(',')[1].replace('CN=','')} for x in res]
    return res

def user_auth(username, password):
    #TODO actually authenticate users
    return {
        'success' : True, 
        'user_type' : 'admin' * ('admin' in username) + 'user' * ('admin' not in username)
    }

def users_last_logins():
    return samba_parser.open_and_parse_log('/var/log/lastlogin.log')

def users_log():
    return samba_parser.open_and_parse_log('/var/log/user.log')

def add_user_to_group(username,group):
    return manage_user_groups(username, [group], action = 'addmembers')


def add_user_to_group2(group,username):
    return manage_user_groups(username, [group], action = 'addmembers')


def rm_user_from_group(username, group):
    #groups = 
    return manage_user_groups(username, [group], action = 'removemembers')

def rm_user_from_group2(group,username):
    #groups = 
    return manage_user_groups(username, [group], action = 'removemembers')


def panel_list_user_groups(username):
    user_groups=[]
    groups = get_groups()
    for group in groups:
        group_members = list_group_members(group[0])
        if username in group_members:
#            user_groups.append({"groupname" : group[0], "description" : group[2], "email" : group[1], "username" : username})
            user_groups.append({"groupname" : group[0], "username" : username})
    return user_groups


def panel_list_user_groups_notmember(username):
    user_groups=[]
    groups = get_groups()
    for group in groups:
        group_members = list_group_members(group[0])
        if username not in group_members:
#            user_groups.append({"groupname" : group[0], "description" : group[2], "email" : group[1], "username" : username})
            user_groups.append({"groupname" : group[0], "username" : username})
    return user_groups

def panel_user_details(username):
    user_details=[]
    data=get_user_data(username)
    
    user_details.append({"username": username, "item" : "First name", "value" : data["first_name"]})
    user_details.append({"username": username, "item" : "Last name", "value" : data["last_name"]})
    user_details.append({"username": username, "item" : "Display name", "value" : data["display_name"]})
    user_details.append({"username": username, "item" : "Description", "value" : data["description"]})
    user_details.append({"username": username, "item" : "Office name", "value" : data["physical_delivery_office_name"]})
    user_details.append({"username": username, "item" : "E-mail", "value" : data["email"]})
    user_details.append({"username": username, "item" : "Phone number", "value" : data["phone"]})
    user_details.append({"username": username, "item" : "Mobile Phone", "value" : data["mobile"]})
    user_details.append({"username": username, "item" : "Home Phone", "value" : data["home_phone"]})
    user_details.append({"username": username, "item" : "Company", "value" : data["company"]})
    user_details.append({"username": username, "item" : "Roaming profile path", "value" : data["profile_path"]})
    user_details.append({"username": username, "item" : "Script path", "value" : data["script_path"]})
    return user_details

def change_user_detail(username, item, new_value):
    attr_map = {
        "First name" : "first_name", 
        "Last name" : "last_name", 
        "Display name" : "display_name", 
        "Description" : "description", 
        "Office name" : "physical_delivery_office_name", 
        "E-mail" : "email", 
        "Phone number" : "phone", 
        "Mobile Phone" : "mobile", 
        "Home Phone" : "home_phone", 
        "Company" : "company", 
        "Roaming profile path" : "profile_path", 
        "Script path" : "script_path", 
   
        
    }
    attr = attr_map[item]
    result = edit_user(username, {attr : new_value})
    return 