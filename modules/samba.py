# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
#import samba_parser

samba_json = { "title": "Add and view users", "content": [ {"type": "Form", "name": "form", "class": "pull-right margina form-inline", "elements": [ {"type": "Filter", "name": "Filter users", "reducers": ["table"]}, { "type": "Button", "name": "Add User", "glyph": "plus", "action": "modal", "reducers": ["modal"], "modal": { "title": "Create an User", "buttons": [ {"type": "Button", "name": "Cancel", "action": "cancel"}, {"type": "Button", "name": "Add user", "class": "primary", "action": "samba.add_user"} ], "content": [ {"type": "Form", "name": "form", "class": "left", "elements": [ {"type": "text", "name": "Username", "value": "", "label": "Username", "required": True}, {"type": "password", "name": "Password", "value": "", "label": "Password", "required": True}, {"type": "text", "name": "Name", "value": "", "label": "Name", "required": True}, {"type": "text", "name": "Surname", "value": "", "label": "Surname", "required": True}, {"type": "checkbox", "name": "vpn", "value": False, "label": "Use VPN", "required": False} ]}, {"type": "Div", "class": "right", "elements": [ {"type": "Heading", "name": "Fill the form to add a new user"}, {"type": "Paragraph", "name": "The new user will be automatically synchronized with Active Directory."} ]}, ] } }, {"type": "Button", "name": "Synchronize cache", "action": "sync_cache"} ]}, {"type": "Table", "name": "table", "reducers": ["table"], "source": "samba.list_users", "columns": [{"key":"username","label":"Username"},{"key":"name","label":"Name"},{"key":"expires","label":"Days since password change"},{"key":"last_login","label":"Last login"},{"key":"comp","label":"Computer"},{"key":"ip","label":"IP address"},{"key":"status","label":"Status"},{"key":"action","label":"Actions"} ], "id":"username", "actions": [ {"name": "Delete Users", "class": "danger", "action": "samba.delete_user"}, {"name": "Change name", "action": "samba.change_name"}, {"name": "Change password", "action": "samba.change_pass"}, {"name": "Lock user", "class": "danger", "action": "samba.lock_user"}, {"name": "Unlock user", "action": "samba.unlock_user"}, {"name": "Manage groups", "action": "samba.manage"} ]} ] }

def get_panel(): 
    panel = ''
#   TODO get from a file
#    with open('/srv/salt/_modules/state_panels/samba.json') as f: 
#        panel = f.read()
    panel = samba_json
    return panel

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



