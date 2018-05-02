install_samba:
  pkg.installed:
    - pkgs:
      - samba
      - krb5-user
      - ntp
      - dnsutils
      - winbind
      - smbclient
      - acl
      - libpam-winbind
      - libnss-winbind
      - ldap-utils
      - ldb-tools
      - swatch

{% set domain = salt['pillar.get']('domain') %}
{% set shortdomain = salt['pillar.get']('shortdomain') %}
{% set admin_password = salt['pillar.get']('admin_password') %}
{% set dcip = '127.0.0.1' %}
{% set host_name = grains['id'] %}
#{% set host_nameXXX = grains['host'] %}

/vapour/data/:
  file.directory:
    - makedirs: True  

/home/_profiles_/:
  file.directory:
    - makedirs: True
    - mode: 777

/home/_public_/:
  file.directory:
    - makedirs: True

install_pip:
  pkg.installed:
    - name: python-pip
    - upgrade: True

install_peewee:
  pip.installed:
    - name: peewee
    - require:
      - pkg: python-pip

/vapour/vapourapps-samba-api.tar.gz:
  file.managed:
    - source: salt://directory/files/vapourapps-samba-api.tar.gz

{% if domain != None %}

/etc/ntp.conf:
  file.append:
    - text:
      - ntpsigndsocket /var/lib/samba/ntp_signd
      - restrict default mssntp

fixownership:
  cmd.run:
    - name: chmod 750 /var/lib/samba/ntp_signd

fixpermissions:
  cmd.run:
    - name: chown root:ntp /var/lib/samba/ntp_signd
    
editresolv:
  cmd.run:
    - name: chattr -i /etc/resolv.conf

/etc/resolv.conf:
  file.managed:
    - source: salt://directory/files/resolv.conf
    - template: jinja
    - context:
      domain: {{ domain }}
      dcip: {{ dcip }} 

resolv-ro:
  cmd.run:
    - name: chattr +i /etc/resolv.conf
      
install_samba-api:
  pip.installed:
    - name: /vapour/vapourapps-samba-api.tar.gz

create_domain:
  cmd.run:
    - name: rm /etc/samba/smb.conf && samba-tool domain provision --use-rfc2307 --use-xattrs=yes --realm {{ domain }} --domain {{ shortdomain }} --server-role dc && touch /vapour/.domain-set
    - onlyif: test ! -e /vapour/.domain-set

setpassword:
  cmd.run:
    - name: samba-tool domain passwordsettings set --complexity=off && samba-tool user setpassword Administrator --newpassword={{ admin_password }}

restorecomplexity:
  cmd.run:
    - name: samba-tool domain passwordsettings set --complexity=on

/etc/samba/smb.conf:
  file.managed:
    - source: salt://directory/files/smb.conf
    - template: jinja
    - context:
      domain: {{ domain }}
      shortdomain: {{ shortdomain }} 
      host_name: {{ host_name }} 

'cp /var/lib/samba/private/krb5.conf /etc/krb5.conf':
  cmd.run

dnsquery_user:
  cmd.run:
    - name: echo "dnsquery:"$(< /dev/urandom tr -dc _1-9A-Z | head -c15)$(< /dev/urandom tr -dc _A-Z-a-z-1-9 | head -c10) > /vapour/dnsquery && samba-tool user add `cat /vapour/dnsquery | tr ':' ' '` --description='VA Bot for DNS Query' --surname='DNS Query' --given-name='VA Bot' && samba-tool group addmembers 'Domain Admins' dnsquery && samba-tool user setexpiry dnsquery --noexpiry 
    - unless: samba-tool user list | grep -q dnsquery

query_user:
  cmd.run:
    - name: samba-tool user add {{salt['pillar.get']('query_user')}} {{salt['pillar.get']('query_password')}} --description='VA Bot for LDAP Query' --surname='LDAP Query' --given-name='VA Bot' && samba-tool user setexpiry {{salt['pillar.get']('query_user')}} --noexpiry
    - unless: samba-tool user list | grep -q '^{{salt['pillar.get']('query_user')}}'

changepsswdpolicy1:
  cmd.run:
    - name: samba-tool domain passwordsettings set --max-pwd-age=0

changepsswdpolicy2:
  cmd.run:
    - name: samba-tool domain passwordsettings set --account-lockout-threshold=7

## exotics    
#/etc/krb5.conf:
#  file.managed:
#    - source: salt://fileshare/files/krb5.conf
#    - user: root
#    - group: root
#    - mode: 644

/etc/sudoers.d/sambatool:
  file.managed:
    - source: salt://directory/files/sambatool
    - user: root
    - group: root
    - mode: 440

/etc/sudoers.d/pdbedit:
  file.managed:
    - source: salt://directory/files/pdbedit
    - user: root
    - group: root
    - mode: 440

/etc/nsswitch.conf:
  file.managed:
    - source: salt://fileshare/files/nsswitch.conf
    - user: root
    - group: root
    - mode: 644

#krb5:
#  file.replace:
#    - name: /etc/krb5.conf
#    - pattern: DOMAIN
#    - repl: {{ domain }}


# shadow should be only compat

nsswitch:
  file.replace:
    - name: /etc/nsswitch.conf
    - pattern: compat
    - repl: compat winbind
    - count: 2
    

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

### these 3 are for last loging tracking:

/root/.swatchrc:
  file.managed:
    - source: salt://directory/files/swatchrc
    - user: root
    - group: root
    - mode: 770

/root/update.sh:
  file.managed:
    - source: salt://directory/files/update.sh
    - user: root
    - group: root
    - mode: 770  

/etc/rc.local:
  file.managed:
    - source: salt://directory/files/rc.local
    - user: root
    - group: root
    - mode: 755

touch /var/log/lastlogin.log:
  cmd.run

#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True

check_functionality_directory:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://directory/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

#### end exotics

restart_samba:
  cmd.run:
    - name: systemctl unmask samba-ad-dc && systemctl start samba-ad-dc && systemctl enable samba-ad-dc
    - watch:
      - file: /etc/samba/smb.conf

{% endif %}

/opt/va-directory/:
  file.directory:
    - makedirs: True

/opt/va-directory/samba.json:
  file.managed:
    - source: salt://directory/files/samba.json

/vapour/winexe_1.00.1-1_amd64.deb:
  file.managed:
    - source: salt://directory/files/winexe_1.00.1-1_amd64.deb

dpkg --install /vapour/winexe_1.00.1-1_amd64.deb:
  cmd.run
#winexe -S on -U TEST/Administrator%P@ssw0rd //192.168.0.1 "cmd.exe"

#shutdown -r +1:
#  cmd.run:
#    - order: last
