# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
import va_samba_api
import json
#import samba_parser


def get_panel(panel_name): 
    panel = ''
    with open('/opt/va-directory/samba.json') as f: 
        samba_json = f.read()
        import json
        samba_json = json.loads(samba_json)
        users_panel = samba_json[panel_name]
        if panel_name == "directory.list_logins":
            return users_panel
        elif panel_name == "directory.overview":
            data1 = panel_get_pass_settings()
            data2 = panel_fsmo_show()
            data3 = panel_get_dc_info()
            data4 = panel_level_show()
            data5 = get_gpo()
            data6 = panel_get_dcs()
            data7 = panel_get_pcs()
            users_panel['tbl_source']['table_pass'] = data1
            users_panel['tbl_source']['table_fsmo'] = data2
            users_panel['tbl_source']['table_info'] = data3
            users_panel['tbl_source']['table_levl'] = data4
            users_panel['tbl_source']['table_gpos'] = data5
            users_panel['tbl_source']['table_domc'] = data6
            users_panel['tbl_source']['table_jpcs'] = data7
            return users_panel
        elif panel_name == "directory.groups":
            arr = va_samba_api.get_groups()
            keys = ["groupname","email","description"]
            data = []
            for x in arr:
                json = {}
                for i, k in enumerate(keys):
                    json[k] = x[i]
                data.append(json)
            users_panel['tbl_source']["table"] = data
            users_panel['tbl_source']["table2"] = []
            return users_panel
        elif panel_name == "directory.org_units":
            arr = va_samba_api.list_organizational_units()
            keys = ["name","description"]
            data = []
            for x in arr:
                json = {}
                for i, k in enumerate(keys):
                    json[k] = x[i]
                data.append(json)
            users_panel['tbl_source']["table"] = data
            return users_panel

        for key in users_panel['tbl_source']:
            tbl = users_panel['tbl_source'][key]
            if "var" in tbl:
                #arr = getattr(va_samba_api, tbl['action'])()[tbl['var']]
                arr = va_samba_api.list_users()['users']
#                return arr
            else:
                arr = getattr(va_samba_api, tbl['action'])()
            if "lbl" in tbl:
                data = [{ tbl['lbl']: x }  for x in arr]
            else:
                data = []
                for x in arr:
                    json = {}
                    for col in list(tbl['cols']):
                        json[col] = x[col]
                    if len(tbl['defaults']) > 0:
                        for d in tbl['defaults']:
                            json[d['key']] = d['value'] 
                    data.append(json)
            users_panel['tbl_source'][key] = data
        panel = {
            panel_name : users_panel
        }[panel_name]
        return panel

def list_users2():
    arr = va_samba_api.list_users()['users']
    cols = ["username", "name", "description", "last_logon", "computer", "ip_address"]
    data = []
    for x in arr:
        d = {}
        for col in cols:
            d[col] = x[col]
        d['status'] = "OK"
        data.append(d)
    return data

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
#o    res = [{'key' : x, 'value'  : res[x]} for x in res]
    return res

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
