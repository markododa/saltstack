import subprocess, re

panel = {"email.user":{"title":"List users","tbl_source":{"table":{}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert"],"columns":[{"key":"user","label":"User"},{"key":"action","label":"Actions"}],"source":"list_users","panels":{"list_rules":"email.rules"},"actions":[{"action":"list_rules","name":"List rules"}],"id":["user"]}]},"email.rules":{"title":"List rules for user ","tbl_source":{"table":{}},"content":[{"type":"Table","name":"table","reducers":["table","panel","alert","modal"],"columns":[{"key":"rule","label":"Rule"},{"key":"action","label":"Actions"}],"source":"list_rules","modals":{"add_rule":{"title":"Add rule","buttons":[{"type":"Button","name":"Cancel","action":"cancel"},{"type":"Button","name":"Add","class":"primary","action":"add_rule"}],"content":[{"type":"Form","name":"form","class":"left","elements":[{"type":"text","name":"Rule","value":"","label":"Rule","required":True}]},{"type":"Div","name":"div","class":"right","elements":[{"type":"Heading","name":"Fill the form to change rule for user"},{"type":"Paragraph","name":"The changed data for user will be automatically synchronized with Email server."}]}]}},"actions":[{"action":"rm_rule","name":"Remove"},{"action":"add_rule","name":"Add rule"}],"id":["rule"]}]}}

def get_panel(panel_name, user = ''):
    ppanel = panel[panel_name]
    return ppanel

#These functions are mostly for helping the actual functions work. YOu can still use them but yeah. 

def postmap_user(user):
    postmap_cmd = ['postmap', '%s.kam.com.mk' % user]
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
        main = re.sub("(smtpd_restriction_classes = .*)", '\\1, %s.kam.com.mk\n\n%s' % (user, user_restriction_line), main)
    elif action == 'rm':
        main = re.sub("(smtpd_restriction_classes = .*)(, %s.kam.com.mk)(.*)" % user, '\\1, \\2', main)
 
    with open('/etc/postfix/main.cf', 'w') as f: 
        f.write(main)

def add_recipient_line(user, recipient):
    with open('/etc/postfix/%s.kam.com.mk' % user, 'a') as f: 
        f.write('\n%s OK' % recipient)

#Above functions are mostly for helping with the actual functions. Those are the ones below. 

def add_email_user_restriction(user):
    touch_file('/etc/postfix/%s.kam.com.mk' % user)
    postmap_user(user)
    change_postfix_restriction(user, action = 'add')
    reload_postfix()

def rm_email_user_restriction(user):
    touch_file('/etc/postfix/%s.kam.com.mk' % user)
    postmap_user(user)
    change_postfix_restriction(user, action = 'rm')
    reload_postfix()

def add_email_user_allowed_recipient(user, recipient):
    add_recipient_line(user, recipient)

    postmap_user(user)
    reload_postfix()


def list_users(): 
    users = ['test1', 'test3', 'test4', 'test5']
    return users
