from va_proxy import *

def __init__(opts):
    # Init global
    va_proxy.__salt__ = __salt__
    va_proxy.proxy_ip = __salt__['pillar.get']('proxy_ip')

from va_proxy_panels import *
