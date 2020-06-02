#The following pillars need to be available for this module to function.
va_email.py:
schema_filter  (schema for ldap AD, if applicable)
use_ldap (set True if mail server uses ldap AD)
return_field (Used only for ldap AD, userPrincipalName or mail) 
query_user (Used only for ldap AD, account to use for query)  
query_password  (Used only for ldap AD, password to use for query user)
va_email_https_fingerprint (Needed for vdirsyncer, fingerprint of self signed https cert) 
