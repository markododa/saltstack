install_samba:
  pkg.installed:
    - pkgs:
      - samba
      - krb5-user
      - ntp
      - nfs-kernel-server 
      - smbclient 
# https://www.stefanwienert.de/blog/2014/07/02/samba-4-active-directory-controller-with-windows-7-roaming-profiles-plus-linux-login-the-definitive-guide/

{% set domain = salt['pillar.get']('domain') %}
{% set adminpass = salt['pillar.get']('adminpass') %}
{% set dcip = salt['pillar.get']('dcip') %}


/etc/krb5.conf:
  file.managed:
    - source: salt://fileshare/krb5.conf
    - user: root
    - group: root
    - mode: 644

/etc/ntp.conf:
  file.managed:
    - source: salt://fileshare/ntp.conf
    - user: root
    - group: root
    - mode: 644

/etc/hosts:
  file.managed:
    - source: salt://fileshare/hosts
    - user: root
    - group: root
    - mode: 644

/etc/resolv.conf:
  file.managed:
    - source: salt://fileshare/resolv.conf
    - user: root
    - group: root
    - mode: 777

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
    - repl: {{ salt['grains.get']('ipv4')[0] }}

hostsmyhostname:
  file.replace:
    - name: /etc/hosts
    - pattern: HOSSST
    - repl: {{ grains['localhost'] }}

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
    
nsswitch:
  file.replace:
    - name: /etc/nsswitch.conf
    - pattern: compat
    - repl: compat winbind

/vapour/:
  file.directory:
    - makedirs: True

{% if domain != None %}

join_domain:
  cmd.run:
    - name: rm /etc/samba/smb.conf && samba-tool domain join {{ domain }} --password={{ adminpass }} -Uadministrator MEMBER && touch /vapour/.fileshare-set
#   - name: rm /etc/samba/smb.conf && samba-tool domain join {{ domain }} --password={{ adminpass }} -Uadministrator --server {{ dcip }} MEMBER && touch /vapour/.fileshare-set
#    - name: rm /etc/samba/smb.conf &&  touch /vapour/.fileshare-set
    - onlyif: test ! -e /vapour/.fileshare-set

{% endif %}

/etc/samba/smb.conf:
  file.managed:
    - source: salt://fileshare/smb.conf
    - user: root
    - group: root
    - mode: 644
    
smb:
  file.replace:
    - name: /etc/samba/smb.conf
    - pattern: DOMAIN
    - repl: {{ domain }}

smbnetbios:
  file.replace:
    - name: /etc/samba/smb.conf
    - pattern: HOST
    - repl: {{ grains['localhost'] }}
