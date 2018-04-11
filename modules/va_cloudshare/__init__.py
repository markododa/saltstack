import va_cloudshare

def __init__(opts):
    # Init global
    va_cloudshare.admin_pass = __salt__['pillar.get']('admin_password')
    va_cloudshare.salt_dict = __salt__


from va_cloudshare import *
from va_cloudshare_panels import *
