# -*- coding: utf-8 -*-
''' Imports all VapourApps API functions into SaltStack'''
import salt, sys
import va_samba_api
from va_samba_api import *
import json
from va_directory_panels import panels


#import samba_parser


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
