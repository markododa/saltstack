install_samba:
  pkg.installed:
    - name: samba


{% set domain = salt['pillar.get']('domain') %}
{% set adminpass = salt['pillar.get']('adminpass') %}

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

install_samba-api:
  pip.installed:
    - name: /vapour/vapourapps-samba-api.tar.gz

#install_samba_api:
#  cmd.run:
#   - name: wget 172.16.0.1:8000/vasambaapi.zip && unzip vasambaapi.zip && cd 

create_domain:
  cmd.run:
    - name: rm /etc/samba/smb.conf && samba-tool domain provision --use-rfc2307 --use-xattrs=yes --realm dc.{{ domain }} --domain {{ domain }} --server-role dc -N && touch /vapour/.domain-set
    - onlyif: test ! -e /vapour/.domain-set
