# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
from va_samba_api import *
#import samba_parser

samba_json = { "title": "Add and view users", "help_url": "", "content": [ {"type": "Form", "elements": [ {"type": "Filter", "name": "Filter users"}, { "type": "Button", "name": "Add User", "glyph": "plus", "action": "modal", "modal": { "title": "Create an User", "buttons": [ {"type": "Button", "name": "Cancel", "action": "cancel"}, {"type": "Button", "name": "Add user", "class": "primary", "action": "samba.add_user"} ], "content": [ {"type": "Div", "class": "left", "elements": [ {"type": "Form", "elements": [ {"type": "Label", "name": "Username"}, {"type": "Input_text", "name": "Username", "required": True}, {"type": "Label", "name": "Password"}, {"type": "Password", "name": "Password", "required": True}, {"type": "Label", "name": "Name"}, {"type": "Input_text", "name": "Name", "required": True}, {"type": "Label", "name": "Surname"}, {"type": "Input_text", "name": "Surname", "required": True}, {"type": "Label", "name": "Use VPN"}, {"type": "Checkbox", "name": "vpn", "required": False} ]} ]}, {"type": "Div", "class": "right", "elements": [ {"type": "Heading", "name": "Fill the form to add a new user"}, {"type": "Paragraph", "name": "The new user will be automatically synchronized with Active Directory."} ]}, ] } }, {"type": "Button", "name": "Synchronize cache", "action": "sync_cache"} ]}, {"type": "Table", "source": "samba.list_users", "columns": ["Username", "Name", "Days since pass change", "Last login", "Computer", "IP address", "Status", "Actions"], "actions": [ {"name": "Delete Users", "class": "warning", "action": "samba.delete_user"}, {"name": "Change name", "action": "samba.change_name"}, {"name": "Change password", "action": "samba.change_pass"}, {"name": "Lock user", "class": "warning", "action": "samba.lock_user"}, {"name": "Unlock user", "action": "samba.unlock_user"}, {"name": "Manage groups", "action": "samba.manage"} ]} ] }

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



