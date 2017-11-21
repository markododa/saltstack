import subprocess, re, netaddr

#2 panels
#panel = {"email.user":{"title":"List users","tbl_source":{"table":{}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"user","label":"User"},{"key":"samaccountname","label":"sAMAccountName"},{"key":"action","label":"Actions"}],"source":"list_users","panels":{"list_rules":"email.rules"},"actions":[{"action":"list_rules","name":"List rules"}],"id":["user"]}]},"email.rules":{"title":"List rules","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","reducers":["panel"],"elements":[{"type":"Button","name":"Add rule","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add rule","refresh_action":"get_user_rules","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":"add_user_recipient"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Rule","value":"","label":"Allow recipient","required":true},{"type":"label","name":"lbl","value":"example:\n- user@kam.com.mk (for particular user)\n- @gmail.com (for whole domain *@gmail.com)"}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]} }, {"type":"Button","name":"Add multiple users","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add rule","refresh_action":"get_user_rules","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":["add_multiple_user_recipients","va-owncloud.kam.com.mk:add_user_contact"]}],"content":[{"type":"Form","name":"form","class":"left","elements":[]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]}}]},{"type":"Table","name":"table","reducers":["table","panel","alert","modal"],"columns":[{"key":"rule","label":"Rule"},{"key":"action","label":"Actions"}],"source":"get_user_rules","actions":[{"action":"rm_user_recipient","name":"Remove"}],"id":["rule"]}]}}

panel={"email.filterlists":{"title":"Mail filterlists","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","reducers":["panel"],"elements":[{"type":"Button","name":"Resend All","glyph":"send","action":"modal","reducers":["modal"],"modal":{"title":"Resend All","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Resend All","class":"primary","action":"force_mail_queue"}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will force resending all unsent items. Are you sure?"}]}]}},{"type":"Button","name":"Clear Queue","glyph":"trash","class":"danger","action":"modal","reducers":["modal"],"modal":{"title":"Clear Queue","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Clear","class":"primary","action":["delete_mail_queue"]}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will remove all unsent messages from the queue. Are you sure?"}]}]}}]},{"type":"Table","name":"table","reducers":["table","alert"],"columns":[{"key":"arrival_time","label":"Time"},{"key":"queue_id","label":"Mail ID"},{"key":"sender","label":"Sender"},{"key":"recipients","label":"Recipients"},{"key":"size","label":"Size (b)"}],},{"type":"Form","name":"form2","class":"tbl-ctrl2","reducers":["panel"],"elements":[{"type":"Button","name":"Resend All","glyph":"send","action":"modal","reducers":["modal"],"modal":{"title":"Resend All","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Resend All","class":"primary","action":"force_mail_queue"}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will force resending all unsent items. Are you sure?"}]}]}},{"type":"Button","name":"Clear Queue","glyph":"trash","class":"danger","action":"modal","reducers":["modal"],"modal":{"title":"Clear Queue","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Clear","class":"primary","action":["delete_mail_queue"]}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will remove all unsent messages from the queue. Are you sure?"}]}]}}]}]},"email.user":{"title":"List users","tbl_source":{"table":{}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"user","label":"User"},{"key":"samaccountname","label":"sAMAccountName"},{"key":"action","label":"Actions"}],"source":"list_users","panels":{"list_rules":"email.rules"},"actions":[{"action":"list_rules","name":"List rules"}],"id":["user"]}]},"email.queue":{"title":"Mail queue","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","reducers":["panel"],"elements":[{"type":"Button","name":"Resend All","glyph":"send","action":"modal","reducers":["modal"],"modal":{"title":"Resend All","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Resend All","class":"primary","action":"force_mail_queue"}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will force resending all unsent items. Are you sure?"}]}]}},{"type":"Button","name":"Clear Queue","glyph":"trash","class":"danger","action":"modal","reducers":["modal"],"modal":{"title":"Clear Queue","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Clear","class":"primary","action":["delete_mail_queue"]}],"content":[{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Confirmation"},{"type":"Paragraph","name":"This will remove all unsent messages from the queue. Are you sure?"}]}]}}]},{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"arrival_time","label":"Time"},{"key":"queue_id","label":"Mail ID"},{"key":"sender","label":"Sender"},{"key":"recipients","label":"Recipients"},{"key":"size","label":"Size (b)"},{"key":"action","label":"Actions"}],"source":"mail_queue","panels":{"list_rules":"email.rules"},"actions":[{"action":"force_mail_queue_id","name":"Send Now"},{"action":"delete_mail_queue_id","name":"Delete","class":"danger"}],"id":["queue_id"]}]},"email.rules":{"title":"List rules","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","reducers":["panel"],"elements":[{"type":"Button","name":"Add rule","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add rule","refresh_action":"get_user_rules","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":"add_user_recipient"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Rule","value":"","label":"Allow recipient","required":True},{"type":"label","name":"lbl","value":"example:\n- user@kam.com.mk (for particular user)\n- @gmail.com (for whole domain *@gmail.com)"}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]}},{"type":"Button","name":"Add multiple users","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add rule","refresh_action":"get_user_rules","table_name":"table","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":["add_multiple_user_recipients","va-owncloud.kam.com.mk:add_user_contact"]}],"content":[{"type":"Form","name":"form","class":"left","elements":[]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]}}]},{"type":"Table","name":"table","reducers":["table","panel","alert","modal"],"columns":[{"key":"rule","label":"Rule"},{"key":"action","label":"Actions"}],"source":"get_user_rules","actions":[{"action":"rm_user_recipient","name":"Remove"}],"id":["rule"]}]}}


def get_panel(panel_name, user = ''):
    ppanel = panel[panel_name]
    if panel_name == "email.user":
        data = list_users()
        ppanel['tbl_source']['table'] = data
    if panel_name == "email.queue":
        data = mail_queue()
        ppanel['tbl_source']['table'] = data
    if panel_name == "email.rules":
        data = get_user_rules(user)
        ppanel['tbl_source']['table'] = data
        checkboxes = [ {"type":"checkbox","name":val['user'],"value":False,"label":val['user'],"required":True} for key,val in enumerate(list_users()) if val['user'] != user]
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
    print 'Touching : ', user_file_path
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

def get_ldap_users(return_field, path = '/etc/dovecot/dovecot-ldap.conf'):
    schema_filter = __salt__['pillar.get']('schema_filter',default='')
    vars = ['hosts', 'dn', 'dnpass', 'base']
    vars = get_conf_vars_file(vars, path)
    if schema_filter != '':
        filter = schema_filter+vars['base']+'))'
    else:
        filter = ''
    cmd = ['ldapsearch', '-x', '-h', vars['hosts'], '-D', vars['dn'], filter, '-b', vars['base'], '-w', vars['dnpass'], 'sAMAccountName', return_field, '-S', 'sAMAccountName']
#    cmd = "ldapsearch '-x' '-h' '{hosts}' '-D' '{dn}' '{filter}' '-b' '{base}' '-w' '{dnpass}' 'sAMAccountName' '{return_field}' '-S' 'sAMAccountName'".format(
#        hosts = vars['hosts'], dn = vars['dn'], filter = filter, base = vars['base'], dnpass = vars['dnpass'], return_field = return_field
#    )
#    return subprocess.list2cmdline([cmd])
    result = subprocess.check_output(cmd)
    result = [x for x in result.split('#')]
    result = [[i for i in x.split('\n') if ':' in i] for x in result]
    result = [dict([i.split(': ') for i in x]) for x in result]
    return result


def list_users(email_domain=''):
    return_field = __salt__['pillar.get']('return_field',default='userPrincipalName')
    if email_domain == '':
        email_domain = email_domains()[0]
    users = get_ldap_users(return_field=return_field)
    result = [{'user' : x.get(return_field), 'samaccountname' : x.get('sAMAccountName')} for x in users if email_domain in x.get(return_field, '')] 
    return result 

def get_wblist(ruleset, direction='inbound', account='@.'):
    array = __salt__['cmd.run']('python /opt/iredapd/tools/wblist_admin.py --'+direction+' --'+account+' --list --'+ruleset).split("\n")
    if len(array) == 3:
       return []
    else:
       return array[2:]

def get_whitelist(ruleset='whitelist',direction='inbound', account='@.'):
    return get_wblist(ruleset)

def get_blacklist(ruleset='blacklist',direction='inbound', account='@.'):
    return get_wblist(ruleset)

def wbmanage(action, ruleset, address, direction='inbound', account='@.'):
    array = address.split(' ')
    for i in range(len(array)):
       if netaddr.valid_ipv4(array[i]) or netaddr.valid_ipv6(array[i]):
           True
       elif '@' not in array[i]:
           array[i] = '@'+array[i]
    address = ' '.join(array)
    return __salt__['cmd.run']('python /opt/iredapd/tools/wblist_admin.py --'+direction+' --'+account+' --'+action+' --'+ruleset+' '+address)

def get_dns_config():
   domains = []
   keys = __salt__['cmd.run']('amavisd-new showkeys').split('; key#')[1:]
   for domain in keys:
       url = ''.join(domain.replace(' '*2,'').split("\n")[1].split('3600')[0])
       dkim = ''.join(domain.replace(' '*2,'').replace('\n','').split('"')[1:-1])
       domains.append(url[0:-1]+' TXT '+dkim)
   return domains

def email_domains():
    return open('/etc/postfix/transport', 'r').read().lower().split(' dovecot\n')

def dovecot_quota():
    return __salt__['cmd.run']('/usr/bin/doveadm -f flow quota get -A')

def mail_queue():
    output =  __salt__['cmd.run']('mailq')
#    output = __salt__['cmd.run']('cat /root/testq.txt')
    output_lines = output.split('\n')[1:-2]
    output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_space_separated = [[i for i in x.split(' ') if i] for x in output_lines_stripped]

    lines_sender_rcpnt_combined = []
    for x in output_lines_space_separated:
        if not x: continue
        if len(x) > 1:
            sender_dict = {
                'queue_id' : x[0].split('*')[0],
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
    return __salt__['cmd.run']('postqueue -f')

def delete_mail_queue():
    return __salt__['cmd.run']('postsuper -d ALL')

def force_mail_queue_id(message_id):
# postqueue -i queue_id
    return __salt__['cmd.run']('postqueue -i '+message_id)

def delete_mail_queue_id(message_id):
# postsuper -d 5642B4D8647 (remove * at the end)
    return __salt__['cmd.run']('postsupr -d '+messsage_id)

def view_mail_queue_id(message_id):
#postcat -vq 5642B4D8647
    return __salt__['cmd.run']('postcat -vq '+messsage_id)

