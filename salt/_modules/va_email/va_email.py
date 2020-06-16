import subprocess, requests, json, re, netaddr
from . import vcards
from va_utils import check_functionality as panel_check_functionality
from .va_email_panels import panels

def dovecot_quota():
    """ api-help: Get used quota for all users. """
    return __salt__['cmd.run']('/usr/bin/doveconf plugin/quota_rule -h').split('=')[1:]

def get_panel(panel_name, user = ''):
    ppanel = panels[panel_name]
    if panel_name == "get_allowed_recipients":
        data = get_allowed_recipients(user)
        ppanel['tbl_source']['table'] = data
        existing = [ x["address"] for x in get_allowed_recipients(user)]
        checkboxes = [ {"type":"checkbox","name":val['username'],"value":False,"label":val["name"]+": "+val['username'],"required":True} for key,val in enumerate(list_users()) if val['username'] not in existing and val['username'] != user ]
        ppanel['content'][0]['elements'][1]['modal']['content'][0]['elements'] = checkboxes
        return ppanel

#These functions are mostly for helping the actual functions work. YOu can still use them but yeah. 

def postmap_user(user):
    postmap_cmd = ['postmap', '/etc/postfix/%s' % user]
    subprocess.check_output(postmap_cmd)

def reload_postfix():
    postfix_cmd = ['service', 'postfix', 'reload']
    subprocess.check_output(postfix_cmd)

def touch_file(file_path):
    open(file_path, 'a').close()

def change_postfix_restriction(user, action = 'add'):
    main = ''
    with open('/etc/postfix/main.cf') as f:
        main = f.read()

    user_restriction_line = '%s =\n    check_recipient_access hash:/etc/postfix/local_domains, reject' % user

    if action == 'add':
        main = re.sub("(smtpd_restriction_classes = .*)", '\\1, %s\n\n%s' % (user, user_restriction_line), main)
    elif action == 'rm':
        main = re.sub("(smtpd_restriction_classes = .*)(, %s)(.*)" % user, '\\1\\3', main)
        main = re.sub('\n' + user + ' =.*\n.*\n', '', main)


    with open('/etc/postfix/main.cf', 'w') as f:
        f.write(main)

def add_recipient_line(user, recipient):
    with open('/etc/postfix/%s' % user, 'a') as f:
        f.write('\n%s OK' % recipient)


def rm_recipient_line(user, recipient):
    rules = ''
    with open('/etc/postfix/' + user, 'r') as f: 
        rules = f.read()
        

    rules = re.sub(recipient + '.*', '', rules)

    with open('/etc/postfix/' + user, 'w') as f: 
        f.write(rules)

#Above functions are mostly for helping with the actual functions. Those are the ones below.

def add_email_user_restriction(user):
    user_file_path = '/etc/postfix/' + user.replace('@', '.')
    # print 'Touching : ', user_file_path
    touch_file(user_file_path)
    postmap_user(user)
    change_postfix_restriction(user, action = 'add')
    reload_postfix()

def rm_email_user_restriction(user):
#    touch_file('/etc/postfix/%s' % user)
    postmap_user(user)
    change_postfix_restriction(user, action = 'rm')
    reload_postfix()

def add_multiple_user_recipients(user, recipient_list):
    for r in recipient_list:
        add_user_recipient(user, r)

def add_user_recipient(user, recipient):
    touch_file(user.replace('@', '.'))
    add_recipient_line(user.replace('@', '.'), recipient)

    postmap_user(user.replace('@', '.'))
    reload_postfix()

def rm_user_recipient(user, recipient):
    rm_recipient_line(user.replace('@', '.'), recipient)

    postmap_user(user.replace('@', '.'))
    reload_postfix()

def get_user_rules(user):
    if not user: return []
    user = user.replace('@', '.')
    rules = ''
    try:
        with open('/etc/postfix/' + user) as f:
            rules = f.read()
    except: 
        return []
    rules = rules.split('\n')
    rules = [{'rule': x.split(' ')[0].split('\t')[0]} for x in rules if x]
    return rules

def get_conf_var(var, conf):
    x = [x for x in conf.split('\n') if var in x] or ['=']
    x = x[0]
    x = x.split(' = ')[1:]
    x = ''.join(x)
    x = x.replace('"', '')
    x = x.rstrip()
#    x = re.sub(var + '.*= (.*)', '\1', conf)
    return x

def get_conf_vars(vars, conf):
    vars = {
        v : get_conf_var(v, conf) for v in vars
    }

    return vars

def get_conf_vars_file(vars, path):
    conf = ''
    with open(path) as f:
        conf = f.read()

    return get_conf_vars(vars, conf)

def get_psql_users():
    return __salt__['postgres.psql_query']("select username,name from mailbox", maintenance_db='vmail')

def get_ldap_users(return_field, path = '/etc/dovecot/dovecot-ldap.conf'):
    return_field = return_field.split(" ")
    """ api-help: Lists all users from the ldap database. """
    schema_filter = __salt__['pillar.get']('schema_filter',default='')
    filter = __salt__['pillar.get']('schema_filter',default='')
    vars = ['hosts', 'dn', 'dnpass', 'base']
    vars = get_conf_vars_file(vars, path)
#    if schema_filter != '':
#        filter = schema_filter+vars['base']+'))'
#    else:
#        filter = ''
    cmd = ['ldapsearch', '-x', '-h', vars['hosts'], '-D', vars['dn'], filter, '-b', vars['base'], '-w', vars['dnpass'], 'sAMAccountName']+return_field+['-S', 'sAMAccountName']
#    cmd = "ldapsearch '-x' '-h' '{hosts}' '-D' '{dn}' '{filter}' '-b' '{base}' '-w' '{dnpass}' 'sAMAccountName' '{return_field}' '-S' 'sAMAccountName'".format(
#        hosts = vars['hosts'], dn = vars['dn'], filter = filter, base = vars['base'], dnpass = vars['dnpass'], return_field = return_field
#    )
#    return subprocess.list2cmdline([cmd])
    result = subprocess.check_output(cmd)
    result = [x for x in result.split('#') if x is not '' and ': ' in x]
    result = [[i for i in x.split('\n') if ': ' in i] for x in result]
    result = [dict([i.split(': ') for i in x]) for x in result]
    return result


def list_users(email_domain=''):
    use_ldap = __salt__['pillar.get']('use_ldap',  False)
    """ 
        description: "Lists all users from an LDAP db. In order to list_users, the function uses a return_field, retrieved from the `return_field` pillar key, with userPrincipalName as a default. Then it makes a list of dictionaries with values based on the returnfield and the sAMAccountName value from LDAP, for instance [{'user' : 'username', 'samaccountname' : 'sAMAccountName'}, ...]. To get these values, we use the `get_ldap_users` function. "
        arguments: 
          email_domain: When the users are retrieved from LDAP, we filter them by this argument. If it is empty, we use the first email_domain returned by the email_domains() function, which reads from '/etc/postfix/transport'
        output: "A list of dictionaries as follows: [{'user' : 'test_user@email_domain', 'samaccountname' : 'test_user'}, {'user' : 'test_user2@email_domain', 'samaccountname' : 'test_user2'}, ...]"
    """
    if use_ldap == True:
        return_field = __salt__['pillar.get']('return_field',default='userPrincipalName')
        if email_domain == '':
            email_domain = email_domains()[0]
        users = get_ldap_users(return_field=return_field+' cn') #NINO treba da gi vraka i grupite vo slucaj koga return_field e userPrincipalName
        result = [{'username' : x.get(return_field), 'accountname' : x.get('sAMAccountName'), 'name': x.get('cn')} for x in users if email_domain in x.get(return_field, '')] 
        return result

    elif use_ldap == False:
        if email_domain == '':
            email_domain = email_domains(use_ldap)[0]
        users = get_psql_users()
        result = [{ 'username': x.get('username'), 'accountname': x.get('username').split('@')[0], 'name': x.get('name')} for x in users if email_domain in x.get('username') ]
        return result
    else:
        return "Please set use_ldap for the server"

def users_in_dict():
    use_ldap = __salt__['pillar.get']('use_ldap',  False)
    users = list_users(email_domain=email_domains(use_ldap)[0])
    result = {}
    for x in users:
        if x.get('username'):
            result[x['username']]={'name': x.get('name'), 'accountname': x.get('accountname')}
    return result


def get_wblist(ruleset, direction='inbound', account='@.'):
    array = __salt__['cmd.run']('python /opt/iredapd/tools/wblist_admin.py --'+direction+' --account '+account+' --list --'+ruleset).split("\n")
    result = [{"address" : x} for x in array[2:]]
    if len(result) == 1 and result[0]['address'] == '* No whitelist/blacklist.':
        return []
    return result

def get_whitelist(ruleset='whitelist',direction='inbound', account='@.'):
    """ api-help: Get whitelisted hosts. """
    return get_wblist(ruleset)

def get_blacklist(ruleset='blacklist',direction='inbound', account='@.'):
    """ api-help: Get blacklisted hosts. """
    return get_wblist(ruleset)

def get_allowed_recipients(account):
    """ api-help: Get allowed recipents for account """
    recipients = get_wblist(ruleset='whitelist',  direction='outbound', account=account)
    minion_id=__salt__['grains.get']('id')
    users_in_dict=__salt__['mine.get'](minion_id, 'email_accounts')[minion_id]
    result = []
    for x in recipients:
        if type(users_in_dict.get(x["address"])) == dict:
            name=users_in_dict.get(x["address"]).get("name","")
        else:
            name=vcards.get_vcard(account,x["address"]).get("FN","")
        result.append({"address": x.get("address"), "name": name})
    return result



def wbmanage(action, ruleset, address, direction='inbound', account='@.'):
# python /opt/iredapd/tools/wblist_admin.py --delete --blacklist 172.16.1.10
# --add --blacklist baduser@example.com
    array = address.split(' ')
    for i in range(len(array)):
        if netaddr.valid_ipv4(array[i]) or netaddr.valid_ipv6(array[i]):
            True
        elif '@' not in array[i]:
            array[i] = '@'+array[i]
    address = ' '.join(array)
    return __salt__['cmd.run']('python /opt/iredapd/tools/wblist_admin.py --'+direction+' --account '+account+' --'+action+' --'+ruleset+' '+address)

def remove_allowed_recipient(account, recipient):
    vcards.remove_vcard(account=account, recipient=recipient)
    return wbmanage(action='delete', ruleset='whitelist', address=recipient, direction='outbound', account=account)

def add_allowed_recipient(account, recipient, name):
    vcards.generate_vcard(account=account, recipient=recipient,name=name)
    return wbmanage(action='add', ruleset='whitelist', address=recipient, direction='outbound', account=account)

def add_allowed_recipients(account, **recipients):
    users_dict=users_in_dict()
    recipients = [ recipient for recipient in recipients if recipients[recipient] == True ]
    recipients_with_names=[{"address": x, "name": users_dict.get(x).get("name","")} for x in recipients]
    vcards.generate_vcards(account=account, recipients=recipients_with_names)
    recipients=' '.join(recipients)
    return wbmanage(action='add', ruleset='whitelist', address=recipients, direction='outbound', account=account)


def add_filter_whitelist(filter=''):
    """ api-help: Add whitelist rule. """
    return wbmanage('add','whitelist',filter)

def add_filter_blacklist(filter=''):
    """ api-help: Add blacklist rule. """
    return wbmanage('add','blacklist',filter)

def delete_filter_whitelist(filter=''):
    """ api-help: Delete whitelist rule. """
    return wbmanage('delete','whitelist',filter)

def delete_filter_blacklist(filter=''):
    """ api-help: Delete blacklist rule. """

    return wbmanage('delete','blacklist',filter)

def panel_get_dns_config():
    domains = []
    keys = __salt__['cmd.run']('amavisd-new showkeys').split('; key#')[1:]
    for domain in keys:
        url = ''.join(domain.replace(' '*2,'').split("\n")[1].split('3600')[0])
        dkim = ''.join(domain.replace(' '*2,'').replace('\n','').split('"')[1:-1])

        result = requests.get('http://ifconfig.co/json')
        public_ip = json.loads(result.text)['ip']
        domains.append({"dns":"va-email."+email_domains()[0],"type":'A',"value":public_ip})
        domains.append({"dns":"va-email."+email_domains()[0],"type":'MX',"value":public_ip})
        domains.append({"dns":"imap.va-email."+email_domains()[0],"type":'CNAME',"value":"va-email."+email_domains()[0]})
        domains.append({"dns":"pop3.va-email."+email_domains()[0],"type":'CNAME',"value":"va-email."+email_domains()[0]})
        domains.append({"dns":"smtp.va-email."+email_domains()[0],"type":'CNAME',"value":"va-email."+email_domains()[0]})
        domains.append({"dns":email_domains()[0],"type":'TXT',"value":"v=spf1 a mx ip4:"+public_ip+" -all"})
        domains.append({"dns":"_dmarc."+email_domains()[0],"type":'TXT',"value":"v=DMARC1; p=none"})
        dkim_multiline=dkim[:74] +'\n' + dkim[74:151]+'\n' + dkim[151:]
        domains.append({"dns":url[0:-1],"type":'TXT',"value":dkim_multiline})

    return domains

def panel_server_config():
    confi = []

    email_field = __salt__['pillar.get']('return_field',default='username')
    if email_field =='username':
        email_field = "Email address is combination of username and domain name '"+email_domains()[0]+"'"
    else:
        email_field = "Email address is read from 'mail' field in Active Directory"        
    confi.append({"key":"Email adresses","value":email_field})
    confi.append({"key":"Default quota","value":dovecot_quota()})

    return confi



def panel_statistics():
    diskusage =__salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /var/vmail/ -o TARGET').split()[1]]
    statistics = [{'key' : 'Mail storage partition used size (MB)', 'value': int(diskusage['used'])/1024},
                {'key' : 'Mail storage partition free space (MB)', 'value': int(diskusage['available'])/1024},
                {'key' : 'Mail storage partition mount point', 'value': diskusage['filesystem']}]
    return statistics

def get_dns_config():
    domains = []
    keys = __salt__['cmd.run']('amavisd-new showkeys').split('; key#')[1:]
    for domain in keys:
        url = ''.join(domain.replace(' '*2,'').split("\n")[1].split('3600')[0])
        dkim = ''.join(domain.replace(' '*2,'').replace('\n','').split('"')[1:-1])
        domains.append(url[0:-1],' TXT ',dkim)
    return domains

def email_domains(use_ldap=True):
    """ api-help: Get provisioned e-mail domains on the mail server. """
    if use_ldap == True:
        return open('/etc/postfix/transport', 'r').read().lower().split(' dovecot\n')
    elif use_ldap == False:
        return [ x['domain'] for x in __salt__['postgres.psql_query']("select domain from domain", maintenance_db='vmail')]



def str_is_error(s):
    return re.search(r'^\(.*\)$', s) is not None

def mail_queue():
    """ api-help: Get the current mail queue. """
    output =  __salt__['cmd.run']('mailq')
#    output = __salt__['cmd.run']('cat /root/testq.txt')
    output_lines = output.split('\n')[1:-2]
    output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_space_separated = [[i for i in x.split(' ') if i] if not str_is_error(x) else x for x in output_lines_stripped]

    lines_sender_rcpnt_combined = []
    for x in output_lines_space_separated:
        if not x: continue
        if type(x) == str:
            lines_sender_rcpnt_combined[-1]['error'] = x
        elif len(x) > 1:
            sender_dict = {
                'queue_id' : x[0].replace('*',''),
                'size' : x[1],
                'arrival_time' : ' '.join(x[2:6]),
                'recipients' : [],
                'sender' : x[6],
            }
            lines_sender_rcpnt_combined.append(sender_dict)
        elif x[0]:
            lines_sender_rcpnt_combined[-1]['recipients'].append(x[0])

    return lines_sender_rcpnt_combined

def log_dovecot():
    return __salt__['cmd.run']('cat /var/log/dovecot.log')


def force_mail_queue():
    #return __salt__['cmd.run']('postqueue -f')
    x = subprocess.call(['/usr/sbin/postqueue', '-f'])

    if x :
        return_message = "Error"
        is_success = False
    else :
        return_message = "Resending messages from Queue."
        is_success = True

    return {"data" : {}, "success" : is_success, "message" : return_message}



def delete_mail_queue():
    """ api-help: Delete the entire email queue. """
    x = subprocess.call(['/usr/sbin/postsuper', '-d' , 'ALL'])

    if x :
        return_message = "Error"
        is_success = False
    else :
        return_message = "Queue is empty now."
        is_success = True

    return {"data" : {}, "success" : is_success, "message" : return_message}

def force_mail_queue_id(message_id):
    """ api-help: Forces a resend of all e-mails in the queue. """
#    return __salt__['cmd.run']('postqueue -i '+message_id)
    x = subprocess.call(['/usr/sbin/postqueue', '-i' , message_id])

    if x :
        return_message = "Error"
        is_success = False
    else :
        return_message = "Resending message with ID "+str(message_id)
        is_success = True

    return {"data" : {}, "success" : is_success, "message" : return_message}

def delete_mail_queue_id(message_id):
    """ api-help: Deletes a single email of the queue by id. """
# postsuper -d 5642B4D8647 
    x = subprocess.call(['/usr/sbin/postsuper', '-d' , message_id])
    #x = __salt__['cmd.run']('postsuper -d '+message_id)

    if x :
        return_message = "Error"
        is_sucess = False
    else :
        return_message = "Removing message with ID "+str(message_id)
        is_sucess = True
    return {"data" : {}, "success" : is_success, "message" : return_message}

def view_mail_queue_id(message_id):
    __salt__['cmd.run']('postcat -vq '+messsage_id)
    return "OK"

def error_mail_queue_id(message_id):
    queue = mail_queue()
    for msg in queue:
        if msg['queue_id']==message_id:
            if msg['error']:
                return {"success" :  False, "message" : msg['error'], "data" : {}}
            else:
                return {"success" :  True, "message" : "So far so good", "data" : {}}

