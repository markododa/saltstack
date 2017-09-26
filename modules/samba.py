# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
import va_samba_api
import json
#import samba_parser

#samba_json = {"directory.org_units": {"title":"Organizational units","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","elements":[{"type":"Button","name":"Add organizational unit","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add an organizational unit","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":"create_organizational_unit"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"unit","value":"","label":"Name","required":True},{"type":"text","name":"description","value":"","label":"Description","required":True}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to add an new organizational unit"},{"type":"Paragraph","name":""}]},]}}]},{"type":"Table","name":"table","reducers":["table","panel","alert"],"subpanels":{"list_members":"backup.list_members"},"columns":[{"key":"name","label":"Name"},{"key":"description","label":"Description","width":"60%"},{"key":"action","label":"Actions"}],"actions":[{"action":"list_members","name":"List members"}],"id":["name"]}]},"directory.list_logins": {"title":"Login list","tbl_source":{"table":{"action":"users_log","var":"info","cols":["date","computer","address"],"source":[{"date":"12.12.2012","computer":"192.168.80.90","address":"192.168.80.90"}]}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"date","label":"Date"},{"key":"computer","label":"Computer"},{"key":"address","label":"IP address"}],"source":"users_log"}]},"directory.dns":{"title":"DNS entries","tbl_source":{"table":{"action":"list_dns","cols":["group_name","type","value"],"defaults":[],"source":{}}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","elements":[{"type":"Button","name":"Add DNS entry","glyph":"plus","action":"modal","reducers":["modal","alert"],"modal":{"title":"Add new DNS entry","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add entry","class":"primary","action":"add_dns"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Entryname","value":"","label":"Entry name","required":False},{"type":"dropdown","name":"Type","value":["A","AAAA","MX","NS","CNAME"],"label":"Type","required":False},{"type":"text","name":"Address","value":"","label":"Address","required":False},]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to add a new DNS entry"},{"type":"Paragraph","name":"The IP must not be added until now. For type A use IPv4, for AAAA use IPv6."}]},]}}]},{"type":"Table","name":"table","reducers":["table","filter","panel","modal","alert","form"],"columns":[{"key":"group_name","label":"Group name"},{"key":"type","label":"Type"},{"key":"value","label":"Value"},{"key":"action","label":"Actions"}],"modals":{"edit_entry":{"title":"Edit DNS entry","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Update entry","class":"primary","action":"dns_update"}],"content":[{"type":"Form","name":"form","class":"left","reducers": ["form"],"elements":[{"type":"readonly_text","name":"Entryname","value":"","label":"Entry name","required":False},{"type":"readonly_text","name":"Type","value":"","label":"Type","required":False},{"type":"text","name":"Address","value":"","label":"Address","required":False},]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Edit the form to update DNS entry"},{"type":"Paragraph","name":"If you leave a blank value, it will not change - the old value will be used."}]},]}},"readonly":{"group_name":"Entryname","type":"Type"},"actions":[{"name":"Edit entry","action":"edit_entry"},{"name":"Delete entry","class":"danger","action":"delete_dns"}],"id":"group_name","source":"list_dns"}]},"directory.users":{ "title": "Add and view users", "tbl_source":{"table":{"action":"list_users", "var": "users", "cols":["username","name","description","last_logon","computer","ip_address"],"defaults":[{"key":"status","value":"OK"}], "val":{}}}, "content": [ {"type":"Form","name":"form","class":"tbl-ctrl","elements":[{ "type": "Button", "name": "Add User", "glyph": "plus", "action": "modal", "reducers": ["modal"], "modal": { "title": "Create an User","table_name": "table","refresh_action": "list_users2", "buttons": [ {"type": "Button", "name": "Cancel", "action": "cancel"}, {"type": "Button", "name": "Add user", "class": "primary", "action": "add_user"} ], "content": [ {"type": "Form", "name": "form", "class": "left", "elements": [ {"type": "text", "name": "Username", "value": "", "label": "Username", "required": True}, {"type": "password", "name": "Password", "value": "", "label": "Password", "required": True}, {"type": "text", "name": "Name", "value": "", "label": "First name", "required": True}, {"type": "text", "name": "Surname", "value": "", "label": "Last name", "required": True}, {"type": "text", "name": "email", "value": "", "label": "E-mail","required": True},{"type": "text", "name": "unit", "value": "", "label": "Organizational unit", "required": True}, {"type": "checkbox", "name": "vpn", "value": False, "label": "Change password at next login", "required": False} ]}, {"type": "Div", "class": "right", "elements": [ {"type": "Heading", "name": "Fill the form to add a new user"}, {"type": "Paragraph", "name": "The new user will be automatically synchronized with Active Directory."} ]} ] } }, {"type": "Button", "name": "Synchronize cache", "action": "sync_cache"}]}, {"type": "Table", "name": "table", "reducers": ["table","filter", "panel", "modal", "alert"], "source": "list_users2", "columns": [{"key":"username","label":"Username"},{"key":"name","label":"Name"},{"key":"description","label":"Description"},{"key":"last_logon","label":"Last login"},{"key":"computer","label":"Computer"},{"key":"ip_address","label":"IP address"},{"key":"status","label":"Status"},{"key":"action","label":"Actions"} ], "id":"username", "modals":{"change_name":{"title":"Change user name","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Change","class":"primary","action":"change_name"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Name","value":"","label":"Name","required":True}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change data for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Active Directory."}]}]},"change_password":{"title":"Change user password","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Change","class":"primary","action":"change_password"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"password","name":"Password","value":"","label":"Password","required":True}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change data for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Active Directory."}]}]},"manage_groups":{"title":"Manage groups","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Submit","class":"primary","action":"manage_groups"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"label","name":"Add user to these groups"},{"type":"multi_checkbox","name":"info","value":False,"label":"Info","required":False},{"type":"multi_checkbox","name":"domain_admins","value":False,"label":"Domain Admins","required":False},{"type":"multi_checkbox","name":"support","value":False,"label":"Support","required":False},{"type":"multi_checkbox","name":"sales","value":False,"label":"Sales","required":False},{"type":"multi_checkbox","name":"dev","value":False,"label":"Dev","required":False},{"type":"multi_checkbox","name":"remote","value":False,"label":"Remote Desktop Users","required":False},{"type":"label","name":"Remove user from these groups"}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Manage groups for user : "}]}]}},"panels":{"list_logins":"directory.list_logins"}, "actions": [ {"name": "Delete Users", "class": "danger", "action": "delete_user"}, {"name":"Change name","action":"change_name"}, {"name":"Change password","action":"change_password"}, {"name": "Lock user", "class": "danger", "action": "lock_user"}, {"name": "Unlock user", "action": "unlock_user"}, {"name": "List logins", "action": "list_logins"}, {"name": "Manage groups", "action": "manage_groups"}, {"name": "Change organizational unit", "action": "manage_groups"} ]} ] },"directory.groups": {"title":"All groups", "tbl_source":{"table":{"action":"get_groups","cols":["groupname","description","email"],"defaults": [],"val":{}},"table2":{"action":"get_groups", "cols":[],"lbl":"groupname","defaults": [],"val":{}}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","elements":[{"type":"Button","name":"Add group","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add a new group","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add group","class":"primary","action":"add_group"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Groupname","value":"","label":"Group name","required":True},]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to add a new group"}]},]}}]},{"type":"Table","name":"table","reducers":["table","filter","panel","alert"],"columns":[{"key":"groupname","label":"Name"},{"key":"description","label":"Description"},{"key":"email","label":"E-mail","width":"10%"},{"key":"action","label":"Actions"}],"actions":[{"name":"List Members","action":"list_group_members"},{"name":"Delete group","class":"danger","action":"delete_group"}],"id":"groupname","source":"get_groups"},{"type":"Button","name":"View more","action":"show","target":"div2","reducers":["div"]},{"type":"Div","name":"div2","class":"hidden","reducers":["div"],"elements":[{"type":"Form","name":"form2","class":"tbl-ctrl","elements":[{"type":"Button","name":"Add group","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add a new group","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add group","class":"primary","action":"add_group"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Groupname","value":"","label":"Group name","required":True},]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to add a new group"},{"type":"Paragraph","name":"Some more text."}]},]}}]},{"type":"Table","name":"table2","reducers":["table","filter","panel","alert"],"columns":[{"key":"groupname","label":"Group Name"},{"key":"action","label":"Actions"}],"actions":[{"name":"List Members","action":"list_group_members"},{"name":"Delete group","class":"danger","action":"delete_group"}],"id":"groupname","source":"get_groups"}]}]        }}


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
