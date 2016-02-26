install_samba:
  pkg.installed:
    - pkgs:
      - samba
      - krb5-user
      - ntp
      - dnsutils
      - winbind

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
    - name: |
        samba-tool domain passwordsettings set --complexity=off
        samba-tool user setpassword Administrator --newpassword={{ admin_password }}

/etc/resolv.conf:
  file.managed:
    - source: salt://directory.files/resolv.conf
    - template: jinja

chattr:
  cmd.run:
    - name: chattr +i /etc/resolv.conf

/etc/samba/smb.conf:
  file.blockreplace:
    - marker_start: '[global]'
    - marker_end: 'workgroup'
    - source: salt://directory/files/config 

        
{% endif %}
