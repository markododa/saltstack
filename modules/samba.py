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
