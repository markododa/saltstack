{% from "backuppc/map.jinja" import backuppc with context %}

{% set os = salt['grains.get']('os', None) %}
{% set os_family = salt['grains.get']('os_family', None) %}
{% set backuppc_password = salt['pillar.get']('admin_password') %}

backuppc:
  pkg.installed:
    - name: {{ backuppc.server.pkg }}

{% if backuppc_password %}
backuppc_htpasswd:
  webutil.user_exists:
    - name: {{ backuppc.server.webuser }} 
    - htpasswd_file: {{ backuppc.server.configdir }}/htpasswd
    - password: {{ backuppc_password }}
    - force: true
    - require:
      - pkg: backuppc
{% endif %}

backuppc_config:
  file.managed:
    - name: {{ backuppc.server.configdir }}/config.pl
    - template: jinja
    - source: salt://backuppc/files/config.pl
    - user: {{ backuppc.server.user }}
    - group: {{ backuppc.server.group }}

{% set multisite = salt['pillar.get']('multisite') %}

{% if multisite != True %}

'rm /etc/apache2/sites-enabled/000-default.conf':
  cmd.run:
    - onlyif: test -e /etc/apache2/sites-enabled/000-default.conf

remove_alias:
  file.replace:
    - name: /etc/apache2/conf-available/backuppc.conf
    - pattern: Alias /backuppc /usr/share/backuppc/cgi-bin/
    - repl: |
        Alias /backuppc/image /usr/share/backuppc/image
        DocumentRoot /usr/share/backuppc/cgi-bin/
apache2:
  service.running:
    - watch:
      - file: /etc/apache2/conf-available/backuppc.conf
{% endif %}


backuppc/pubkey:
  event.send:
    - data:
        pubkey: {{salt['cmd.run']('su -s /bin/bash -c "test -e /var/lib/backuppc/.ssh/id_rsa || ssh-keygen -q -f /var/lib/backuppc/.ssh/id_rsa -N \'\' && cat /var/lib/backuppc/.ssh/id_rsa.pub" -l backuppc') }}
    - require:
      - pkg: backuppc

/usr/share/backuppc/lib/BackupPC/CGI/JSON.pm:
  file.managed:
    - source: salt://backuppc/files/JSON.pm

libjson-perl:
  pkg.installed: []

libxml-rss-perl:
  pkg.installed: []

/usr/share/backuppc/lib/realindex.cgi:
  file.blockreplace:
    - marker_start: '"rss"                        => "RSS",' 
    - marker_end: ');'
    - content: '    "json"                       => "JSON",'

/dev/vdb:
  blockdev.formatted

/mnt/va-backup:
  mount.mounted:
    - device: /dev/vdb
    - fstype: ext4
    - mkmnt: True

'mv /var/lib/backuppc /mnt/va-backup/':
  cmd.run:
    - unless: test -e /mnt/va-backup/backuppc

/var/lib/backuppc:
  file.symlink:
    - target: /mnt/va-backup/backuppc

backuppc-restart:
  service.running:
    - name: backuppc
    - watch:
      - file: /var/lib/backuppc

salt/backup/installed:
  event.send
