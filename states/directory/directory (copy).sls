install_samba:
  pkg.installed:
    - pkgs:
      - samba
      - krb5-user
      - ntp
      - dnsutils
      - winbind
      - smbclient

{% set domain = salt['pillar.get']('domain') %}
{% set shortdomain = salt['pillar.get']('shortdomain') %}
{% set admin_password = salt['pillar.get']('admin_password') %}
  
/vapour/data/:
  file.directory:
    - makedirs: True

install_pip:
  pkg.installed:
    - name: python-pip

install_peewee:
  pip.installed:
    - name: peewee
    - require:
      - pkg: python-pip

/vapour/vapourapps-samba-api.tar.gz:
  file.managed:
    - source: salt://directory/files/vapourapps-samba-api.tar.gz

/etc/ntp.conf:
  file.append:
    - text:
      - ntpsigndsocket /usr/local/samba/var/lib/ntp_signd/
      - restrict default mssntp
    
{% if domain != None %}

      
install_samba-api:
  pip.installed:
    - name: /vapour/vapourapps-samba-api.tar.gz

create_domain:
  cmd.run:
    - name: rm /etc/samba/smb.conf && samba-tool domain provision --use-rfc2307 --use-xattrs=yes --realm {{ domain }} --domain {{ shortdomain }} --server-role dc -N && touch /vapour/.domain-set
    - onlyif: test ! -e /vapour/.domain-set

setpassword:
  cmd.run:
    - name: samba-tool domain passwordsettings set --complexity=off && samba-tool user setpassword Administrator --newpassword={{ admin_password }}

/etc/resolv.conf:
  file.managed:
    - source: salt://directory/files/resolv.conf
    - template: jinja
    - context:
      domain: {{ domain }}

chattr:
  cmd.run:
    - name: chattr +i /etc/resolv.conf

/etc/samba/smb.conf:
  file.managed:
    - source: salt://directory/files/smb.conf
    - template: jinja
    - context:
      domain: {{ domain }}
      shortdomain: {{ shortdomain }} 

'cp /var/lib/samba/private/krb5.conf /etc/krb5.conf':
  cmd.run

dnsquery_user:
  cmd.run:
    - name: echo "dnsquery:`openssl rand -hex 10`" > /vapour/dnsquery && samba-tool user add `cat /vapour/dnsquery | tr ':' ' '`
    - unless: test -e /vapour/dnsquery

    
## exotics    
/etc/krb5.conf:
  file.managed:
    - source: salt://fileshare/files/krb5.conf
    - user: root
    - group: root
    - mode: 644

/etc/nsswitch.conf:
  file.managed:
    - source: salt://fileshare/files/nsswitch.conf
    - user: root
    - group: root
    - mode: 644

krb5:
  file.replace:
    - name: /etc/krb5.conf
    - pattern: DOMAIN
    - repl: {{ domain }}

nsswitch:
  file.replace:
    - name: /etc/nsswitch.conf
    - pattern: compat
    - repl: compat winbind

nsswitchw2:
  file.replace:
    - name: /etc/nsswitch.conf
    - pattern: winbind winbind
    - repl: winbind
    
/etc/pam.d/common-account:
  file.managed:
    - source: salt://fileshare/files/common-account
    - user: root
    - group: root
    - mode: 644
    
/etc/pam.d/common-auth:
  file.managed:
    - source: salt://fileshare/files/common-auth
    - user: root
    - group: root
    - mode: 644
    
/etc/pam.d/common-password:
  file.managed:
    - source: salt://fileshare/files/common-password
    - user: root
    - group: root
    - mode: 644
    
/etc/pam.d/common-session:
  file.managed:
    - source: salt://fileshare/files/common-session
    - user: root
    - group: root
    - mode: 644
    
/etc/pam.d/common-session-noninteractive:
  file.managed:
    - source: salt://fileshare/files/common-session-noninteractive
    - user: root
    - group: root
    - mode: 644

#### end exotics
    
restart_samba:
  cmd.run:
    - name: /etc/init.d/samba restart
    - watch:
      - file: /etc/samba/smb.conf
        
{% endif %}
