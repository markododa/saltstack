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
     # - nfs-kernel-server 
     
# https://www.stefanwienert.de/blog/2014/07/02/samba-4-active-directory-controller-with-windows-7-roaming-profiles-plus-linux-login-the-definitive-guide/

{% set domain = salt['pillar.get']('domain') %}
{% set admin_password = salt['pillar.get']('admin_password') %}

## Looping directory minions, looping all network cards, looping first ip address per interface, testing for samba, testing for DNS, updating okdcip if reachable DC from the minion is found
{% set okdcip = {'okdcip': 'unknown'} %}
{% set dcs = salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain').keys() %}
{% for dc in dcs %}
{% set ifaces=salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain')[dc]['ip4_interfaces'].keys() %}
##dc-{{dc}}:
##  ifaces-{{dc}}: {{ifaces}}
    {% for iface in ifaces %}
    {% set ip = salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain')[dc]['ip4_interfaces'][iface][0] %}

    {% if ip != '127.0.0.1' %}
    {% if salt['network.connect'](ip, 139).result %}
    {% if salt['dnsutil.A'](domain, ip) %}
##  okip-{{dc}}-{{iface}}: {{ip}}
    {% do okdcip.update({'okdcip': ip}) %}
    {% endif %}
    {% endif %}
    {% endif %}
    {% endfor %}
{% endfor %}
{% set dcip=okdcip.okdcip %}

## End of looking for DC ip
{% set shortdomain = salt['pillar.get']('shortdomain') %}
{% set host_name = grains['id'] %}

{% set myip=salt['network.get_route'](dcip).source %}

/etc/krb5.conf:
  file.managed:
    - source: salt://fileshare/files/krb5.conf
    - user: root
    - group: root
    - mode: 644

/etc/ntp.conf:
  file.managed:
    - source: salt://fileshare/files/ntp.conf
    - user: root
    - group: root
    - mode: 644
    
/etc/nsswitch.conf:
  file.managed:
    - source: salt://fileshare/files/nsswitch.conf
    - user: root
    - group: root
    - mode: 644

/etc/hosts:
  file.managed:
    - source: salt://fileshare/files/hosts
    - user: root
    - group: root
    - mode: 644

#writableresolve:
#  cmd.run:
#    - name: chattr -i /etc/resolv.conf


/etc/resolv.conf:
  file.managed:
    - source: salt://fileshare/files/resolv.conf
    - user: root
    - group: root
    - mode: 777

resolv:
  file.replace:
    - name: /etc/resolv.conf
    - pattern: DOMAIN
    - repl: {{ domain }}

resolvednsip:
  file.replace:
    - name: /etc/resolv.conf
    - pattern: DCIP
    - repl: {{ dcip }}
    
#readableresolve:
#  cmd.run:
#    - name: chattr +i /etc/resolv.conf 
 
   
ntpcnf:
  file.replace:
    - name: /etc/ntp.conf
    - pattern: DCIP
    - repl: {{ dcip }}

krb5:
  file.replace:
    - name: /etc/krb5.conf
    - pattern: DOMAIN
    - repl: {{ domain }}
    
hosts:
  file.replace:
    - name: /etc/hosts
    - pattern: DOMAIN
    - repl: {{ domain }}
    

hostsmyip:
  file.replace:
    - name: /etc/hosts
    - pattern: MYIP
    - repl: {{ myip }}

    
hostsmyhostname:
  file.replace:
    - name: /etc/hosts
    - pattern: HOSSST
    - repl: {{ grains['localhost'] }}


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
    
/vapour/:
  file.directory:
    - makedirs: True

/home/{{ domain }}/Public/:
  file.directory:
    - makedirs: True
    - mode: 777

/home/{{ domain }}/Public/Tools/:
  file.directory:
    - makedirs: True
    - mode: 777
    
/home/{{ domain }}/Share/:
  file.directory:
    - makedirs: True
    - mode: 777

/home/{{ domain }}/Share/.recycle:
  file.directory:
    - makedirs: True
    - mode: 770
    
/home/{{ domain }}/Public/Tools/tools.tar.gz:
  file.managed:
    - source: salt://fileshare/wintools/tools.tar.gz
    - user: root
    - group: root
    - mode: 644        

extracttools:
  cmd.run:
    - name: tar -xf /home/{{ domain }}/Public/Tools/tools.tar.gz -C /home/{{ domain }}/Public/Tools ; chown Administrator:'domain users' -R /home/{{ domain }}/Public/Tools ; chmod 755 -R /home/{{ domain }}/Public/Tools/
  
fixbat_server:
  file.replace:
    - name: /home/{{ domain }}/Public/Tools/server.bat
    - pattern: DCIP
    - repl: {{ dcip }}     

fixbat_server2:
  file.replace:
    - name: /home/{{ domain }}/Public/Tools/server.bat
    - pattern: DOMEJN
    - repl: {{ shortdomain }}      

fixbat_mp:
  file.replace:
    - name: /home/{{ domain }}/Public/Tools/mp.bat
    - pattern: DOMEJN
    - repl: {{ shortdomain }}   
    
fixbat_mt:
  file.replace:
    - name: /home/{{ domain }}/Public/Tools/mt.bat
    - pattern: DOMEJN
    - repl: {{ shortdomain }}
    

/etc/samba/smb.conf:
  file.managed:
    - source: salt://fileshare/files/smb.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      domain: {{ domain }}
      shortdomain: {{ shortdomain }} 
      host_name: {{ host_name }} 
      
#smb:
#  file.replace:
#    - name: /etc/samba/smb.conf
#    - pattern: DOMAIN
#    - repl: {{ domain }}

#smbnetbios:
#  file.replace:
#    - name: /etc/samba/smb.conf
#    - pattern: HOST
#    - repl: {{ grains['localhost'] }}

#smbshortdm:
#  file.replace:
#    - name: /etc/samba/smb.conf
#   - pattern: DOMEJN
#    - repl: {{ shortdomain }}   
    
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
    
#### functionality script
/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://fileshare/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755
    
{% if domain != None %}

reloadsmbconf:
  cmd.run:
    - name: smbcontrol all reload-config
    - onlyif: test -e /etc/samba/smb.conf
        
join_domain:
  cmd.run:
    - name: net ads join -U Administrator%{{ admin_password }} && touch /vapour/.fileshare-set && shutdown -r +1 "<< Reboot needed after joining domain >>" &
    - onlyif: test ! -e /vapour/.fileshare-set

{% endif %}

/dev/vdb:
  blockdev.formatted

/mnt/va-fileshare:
  mount.mounted:
    - device: /dev/vdb
    - fstype: ext4
    - mkmnt: True

'mv /home /mnt/va-fileshare/':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-fileshare/
        - test ! -e /mnt/va-fileshare/home
        - mount | grep -q /mnt/va-fileshare

'ln -sfn /mnt/va-fileshare/home /home':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-fileshare/home
        - mount | grep -q /mnt/va-fileshare
