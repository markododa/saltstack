import subprocess, re

def postmap_user(user):
    postmap_cmd = ['postmap', '%s.kam.com.mk' % user]
    subprocess.check_output(postmap_cmd)

def reload_postfix():
    postfix_cmd = ['service', 'postfix', 'reload']
    subprocess.check_output(postfix_cmd)

def touch_file(file_path):
    open(file_path, 'a').close()

def add_postfix_restriction(user):
    main = ''
    with open('/etc/postfix/main.cf') as f: 
        main = f.read()

    user_restriction_line = '%s =\n    check_recipient_access hash:/etc/postfix/local_domains, reject' % user

    main = re.sub("(smtpd_restriction_classes = .*)", '\\1, %s.kam.com.mk\n\n%s' % (user, user_restriction_line), main)

    with open('/etc/postfix/main.cf', 'w') as f: 
        f.write(main)

def add_recipient_line(user, recipient):
    with open('/etc/postfix/%s.kam.com.mk' % user, 'a') as f: 
        f.write('\n%s OK' % recipient)

def add_email_user_restriction(user):
    touch_file('/etc/postfix/%s.kam.com.mk' % user)
    postmap_user(user)
    add_postfix_restriction(user)
    reload_postfix()

def add_email_user_allowed_recipient(user, recipient):
    add_recipient_line(user, recipient)
    postmap_user(user)
    reload_postfix()
