install_samba:
  pkg.installed:
    - pkgs:
      - nut

      # COMMANDS
         
      # sudo upsdrvctl start
      # sudo service nut-server status
      # upsc openstackups
      # upscmd l openstackups

{% set myip = salt['grains.get']('ipv4')[0] %}

# needs to find the interface where other upsmonitors are

{% if myip == '127.0.0.1' %}    
{% set myip = salt['grains.get']('ipv4')[1] %}
{% endif %}    

{% if myip == '127.0.0.1' %}    
{% set myip = salt['grains.get']('ipv4')[2] %}
{% endif %}    

/etc/nut/ups.conf:
  file.managed:
    - source: salt://extras/upsmon/ups.conf
    - user: nut
    - group: nut
    - mode: 644

/etc/nut/nut.conf:
  file.managed:
    - source: salt://extras/upsmon/nut.conf
    - user: nut
    - group: nut
    - mode: 644
    
/etc/nut/upsd.users:
  file.managed:
    - source: salt://extras/upsmon/upsd.users
    - user: nut
    - group: nut
    - mode: 640

/etc/nut/upsmon.conf:
  file.managed:
    - source: salt://extras/upsmon/upsmon.conf
    - user: nut
    - group: nut
    - mode: 640
    



# resolvednsip:
  # file.replace:
    # - name: /etc/resolv.conf
    # - pattern: DCIP
    # - repl: {{ dcip }}
    
# readableresolve:
  # cmd.run:
    # - name: chattr +i /etc/resolv.conf 
 
   
# ntpcnf:
  # file.replace:
    # - name: /etc/ntp.conf
    # - pattern: DCIP
    # - repl: {{ dcip }}

# krb5:
  # file.replace:
    # - name: /etc/krb5.conf
    # - pattern: DOMAIN
    # - repl: {{ domain }}
    
# hosts:
  # file.replace:
    # - name: /etc/hosts
    # - pattern: DOMAIN
    # - repl: {{ domain }}
    

# hostsmyip:
  # file.replace:
    # - name: /etc/hosts
    # - pattern: MYIP
    # - repl: {{ myip }}

    
# hostsmyhostname:
  # file.replace:
    # - name: /etc/hosts
    # - pattern: HOSSST
    # - repl: {{ grains['localhost'] }}


# nsswitch:
  # file.replace:
    # - name: /etc/nsswitch.conf
    # - pattern: compat
    # - repl: compat winbind

# nsswitchw2:
  # file.replace:
    # - name: /etc/nsswitch.conf
    # - pattern: winbind winbind
    # - repl: winbind
    
# /vapour/:
  # file.directory:
    # - makedirs: True

# /home/{{ domain }}/Public/:
  # file.directory:
    # - makedirs: True
    # - mode: 777

# /home/{{ domain }}/Public/Tools/:
  # file.directory:
    # - makedirs: True
    # - mode: 777
    
# /home/{{ domain }}/Share/:
  # file.directory:
    # - makedirs: True
    # - mode: 777

# /home/{{ domain }}/Public/Tools/tools.tar.gz:
  # file.managed:
    # - source: salt://fileshare/wintools/tools.tar.gz
    # - user: root
    # - group: root
    # - mode: 644        

# extracttools:
  # cmd.run:
    # - name: tar -xf /home/{{ domain }}/Public/Tools/tools.tar.gz -C /home/{{ domain }}/Public/Tools ; chown Administrator:'domain users' -R /home/{{ domain }}/Public/Tools ; chmod 755 -R /home/{{ domain }}/Public/Tools/
  
# fixbat_mp:
  # file.replace:
    # - name: /home/{{ domain }}/Public/Tools/mp.bat
    # - pattern: DOMEJN
    # - repl: {{ shortdomain }}   
    
# fixbat_mt:
  # file.replace:
    # - name: /home/{{ domain }}/Public/Tools/mt.bat
    # - pattern: DOMEJN
    # - repl: {{ shortdomain }}
    
# /etc/samba/smb.conf:
  # file.managed:
    # - source: salt://fileshare/smb.conf
    # - user: root
    # - group: root
    # - mode: 644
    
# smb:
  # file.replace:
    # - name: /etc/samba/smb.conf
    # - pattern: DOMAIN
    # - repl: {{ domain }}

# smbnetbios:
  # file.replace:
    # - name: /etc/samba/smb.conf
    # - pattern: HOST
    # - repl: {{ grains['localhost'] }}

# smbshortdm:
  # file.replace:
    # - name: /etc/samba/smb.conf
    # - pattern: DOMEJN
    # - repl: {{ shortdomain }}

       
    
# /etc/pam.d/common-account:
  # file.managed:
    # - source: salt://fileshare/common-account
    # - user: root
    # - group: root
    # - mode: 644
    
# /etc/pam.d/common-auth:
  # file.managed:
    # - source: salt://fileshare/common-auth
    # - user: root
    # - group: root
    # - mode: 644
    
# /etc/pam.d/common-password:
  # file.managed:
    # - source: salt://fileshare/common-password
    # - user: root
    # - group: root
    # - mode: 644
    
# /etc/pam.d/common-session:
  # file.managed:
    # - source: salt://fileshare/common-session
    # - user: root
    # - group: root
    # - mode: 644
    
# /etc/pam.d/common-session-noninteractive:
  # file.managed:
    # - source: salt://fileshare/common-session-noninteractive
    # - user: root
    # - group: root
    # - mode: 644
    
    
# {% if domain != None %}

# reloadsmbconf:
  # cmd.run:
    # - name: smbcontrol all reload-config
    # - onlyif: test -e /etc/samba/smb.conf
        
# join_domain:
  # cmd.run:
    # - name: net ads join -U Administrator%{{ admin_password }} && touch /vapour/.fileshare-set && shutdown -r +1 "<< Reboot needed after joining domain >>" &
    # - onlyif: test ! -e /vapour/.fileshare-set

# {% endif %}

    
#reloadsmbd:
#  cmd.run:
#    - name: service smbd restart
#    - onlyif: test -e /etc/samba/smb.conf      
    
#reloadnmbd:
#  cmd.run:
#    - name: service nmbd restart
#    - onlyif: test -e /etc/samba/smb.conf    
    
