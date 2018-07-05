from va_rest import *

def __init__(opts):
    # Init global
    va_rest.__salt__ = __salt__
    # va_rest.rest_ip = __salt__['pillar.get']('proxy_ip')

from va_rest_panels import *
