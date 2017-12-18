# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
import va_samba_api
import json
from va_utils import check_functionality as panel_check_functionality


#import samba_parser


panel_list_dns = list_dns

def panel_list_users():
    return list_users()['users']

def panel_get_groups():
    groups = get_groups()
    groups = [{"groupname" : x[0], "description" : x[2], "email" : x[1]} for x in groups]
    return groups

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
