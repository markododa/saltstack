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


/etc/backuppc/hosts:
  file.line:
    - content: localhost
    - mode: delete


create_key:
  cmd.run:
    - name: su -s /bin/bash -c "ssh-keygen -q -f /var/lib/backuppc/.ssh/id_rsa -N ''" -l backuppc
    - require:
      - pkg: backuppc
    - onlyif: test ! -e /var/lib/backuppc/.ssh/id_rsa

push-key:
  cmd.run:
    - name: salt-call event.send  backuppc/pubkey pubkey="`cat /var/lib/backuppc/.ssh/id_rsa.pub`"
    - onlyif: test -e /var/lib/backuppc/.ssh/id_rsa

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
    - opts: defaults,noatime

'mv /var/lib/backuppc /mnt/va-backup/':
  cmd.run:
    - onlyif:
      - test -e /mnt/va-backup/
      - test ! -e /mnt/va-backup/backuppc
      - mount | grep -q /mnt/va-backup

'ln -sfn /mnt/va-backup/backuppc /var/lib/backuppc':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-backup/backuppc
        - mount | grep -q /mnt/va-backup


#### functionality script
/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://backuppc/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

backuppc-restart:
  service.running:
    - name: backuppc
    - watch:
      - event: salt/backup/installed

salt/backup/installed:
  event.send
