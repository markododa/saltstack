install_samba:
  pkg.installed:
    - pkgs:
      - samba
      - krb5-user
      - ntp
      - dnsutils
      - winbind
      - smbclient
      - swatch
      - libnss-winbind
      - libpam-winbind
      - ldb-tools

{% set domain = salt['pillar.get']('domain') %}
{% set shortdomain = salt['pillar.get']('shortdomain') %}
{% set admin_password = salt['pillar.get']('admin_password') %}
{% set dcip = salt['pillar.get']('dcip') %}
  
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

/etc/resolv.conf:
  file.managed:
    - source: salt://directory/files/resolv.conf
    - template: jinja
    - context:
      domain: {{ domain }}
      dcip: {{ dcip }} 

chattr:
  cmd.run:
    - name: chattr +i /etc/resolv.conf
      
install_samba-api:
  pip.installed:
    - name: /vapour/vapourapps-samba-api.tar.gz

create_domain:
  cmd.run:
    - name: rm /etc/samba/smb.conf && samba-tool domain join {{ shortdomain }} DC -U Administrator%{{ admin_password }} --realm {{ domain }} && touch /vapour/.domain-set
    - onlyif: test ! -e /vapour/.domain-set

# setpassword:
  # cmd.run:
    # - name: samba-tool domain passwordsettings set --complexity=off && samba-tool user setpassword Administrator --newpassword={{ admin_password }}

/etc/samba/smb.conf:
  file.managed:
    - source: salt://directory/files/smb.conf
    - template: jinja
    - context:
      domain: {{ domain }}
      shortdomain: {{ shortdomain }} 

'cp /var/lib/samba/private/krb5.conf /etc/krb5.conf':
  cmd.run

 #check if this user alrady exist?
dnsquery_user:
  cmd.run:
    - name: echo "dnsquery:"$(< /dev/urandom tr -dc '@#$.' | head -c4)$(< /dev/urandom tr -dc _1-9-A-Z | head -c10)$(< /dev/urandom tr -dc _A-Z-a-z-1-9 | head -c10) > /vapour/dnsquery && samba-tool user add `cat /vapour/dnsquery | tr ':' ' '` && samba-tool group addmembers 'Domain Admins' dnsquery && samba-tool user setexpiry dnsquery --noexpiry
    - unless: test -e /vapour/dnsquery

query_user:
  cmd.run:
    - name: samba-tool user add {{salt['pillar.get']('query_user')}} {{salt['pillar.get']('query_password')}} && samba-tool user setexpiry {{salt['pillar.get']('query_user')}} --noexpiry
   
changepsswdpolicy:
  cmd.run:
    - name: samba-tool domain passwordsettings set --max-pwd-age=0
    
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
    
nopdc:
  file.replace:
    - name: /etc/samba/smb.conf
    - pattern: domain master = yes
    - repl: domain master = no
    
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

#### end exotics
    
restart_samba:
  cmd.run:
    - name: /etc/init.d/samba restart
    - watch:
      - file: /etc/samba/smb.conf
        
{% endif %}

/vapour/winexe_1.00.1-1_amd64.deb:
  file.managed:
    - source: salt://directory/files/winexe_1.00.1-1_amd64.deb
    
dpkg --install /vapour/winexe_1.00.1-1_amd64.deb:
  cmd.run
#winexe -S on -U TEST/Administrator%P@ssw0rd //192.168.0.1 "cmd.exe"

shutdown -r +1:
  cmd.run