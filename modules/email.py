import subprocess, re

panel = {"email.user":{"title":"List users","tbl_source":{"table":{}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"user","label":"User"},{"key":"action","label":"Actions"}],"source":"list_users","panels":{"list_rules":"email.rules"},"actions":[{"action":"list_rules","name":"List rules"}],"id":["user"]}]},"email.rules":{"title":"List rules","tbl_source":{"table":{}},"content":[{"type":"Form","name":"form","class":"tbl-ctrl","reducers":["panel"],"elements":[{"type":"Button","name":"Add rule","glyph":"plus","action":"modal","reducers":["modal"],"modal":{"title":"Add rule","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":"add_user_recipient"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Rule","value":"","label":"Rule","required":True}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]} }]},{"type":"Table","name":"table","reducers":["table","panel","alert","modal"],"columns":[{"key":"rule","label":"Rule"},{"key":"action","label":"Actions"}],"source":"list_rules","actions":[{"action":"rm_user_recipient","name":"Remove"}],"id":["rule"]}]}}

def get_panel(panel_name, user = ''):
    ppanel = panel[panel_name]
    if panel_name == "email.user":
        data = [ {'user': x} for x in list_users() ]
        ppanel['tbl_source']['table'] = data
    if panel_name == "email.rules":
        data = get_user_rules(user)
        data = [ {'rule': x} for x in data]
        ppanel['tbl_source']['table'] = data
    return ppanel

#These functions are mostly for helping the actual functions work. YOu can still use them but yeah. 

def postmap_user(user):
    postmap_cmd = ['postmap', '%s' % user]
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
    user_file_path = '/etc/postfix/' + user
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

def add_user_recipient(user, recipient):
    add_recipient_line(user, recipient)

    postmap_user(user)
    reload_postfix()

def rm_user_recipient(user, recipient):
    rm_recipient_line(user, recipient)

    postmap_user(user)
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
    rules = [x.split(' ')[0].split('\t')[0] for x in rules if x]
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

def get_ldap_users(path = '/etc/dovecot/dovecot-ldap.conf'):
    vars = ['hosts', 'dn', 'dnpass']
    vars = get_conf_vars_file(vars, path)

    cmd = ['ldapsearch', '-x', '-h', vars['hosts'], '-D', vars['dn'], '-b', 'dc=kamdooel,dc=local', '-w', vars['dnpass'], 'sAMAccountName', 'mail', '-S', 'sAMAccountName']#, '"(&(mail=%u)(objectClass=person)"']
    result = subprocess.check_output(cmd)
    result = [x for x in result.split('#')]
    result = [[i for i in x.split('\n') if ':' in i] for x in result]
    result = [dict([i.split(': ') for i in x]) for x in result]
    return result


def list_users(email_domain = 'kam.com.mk'):
    users = get_ldap_users()
    result = [x.get('mail') for x in users if email_domain in x.get('mail', '')] 
    return result 


