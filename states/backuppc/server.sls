{% from "backuppc/map.jinja" import backuppc with context %}

{% set os = salt['grains.get']('os', None) %}
{% set os_family = salt['grains.get']('os_family', None) %}
{% set backuppc_password = salt['pillar.get']('backuppc:server:backuppc_password', salt['grains.get']('server_id')) %}

{% if backuppc_password %}
{% if os_family == 'Debian' %}
backuppc_debconf_utils:
  pkg.installed:
    - name: {{ backuppc.server.debconf_utils }}

backuppc_debconf:
  debconf.set:
    - name: backuppc
    - data: 
        'backuppc/tmppass': {'type': 'password', 'value': '{{ backuppc_password }}'}
    - require_in:
      - pkg: backuppc
    - require:
      - pkg: backuppc_debconf_utils
{% elif os_family == 'RedHat' or 'Suse' %}
backuppc_htpasswd:
  webutil.user_exists:
    - name: {{ backuppc.server.webuser }} 
    - htpasswd_file: {{ backuppc.server.configdir }}/htpasswd
    - option: d
    - force: true
{% endif %}
{% endif %}

backuppc:
  pkg.installed:
    - name: {{ backuppc.server.pkg }}
    {% if os_family == 'Debian' and backuppc_password %}
    - require:
      - debconf: backuppc_debconf
    {% endif %}

backuppc_config:
  file.managed:
    - name: {{ backuppc.server.configdir }}/config.pl
    - template: jinja
    - source: salt://backuppc/files/config.pl
    - user: {{ backuppc.server.user }}
    - group: {{ backuppc.server.group }}

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
    - reload: True
    - watch:
      - file: /etc/apache2/conf-available/backuppc.conf

generate_ssh-key:
  cmd.run:
    - name: ssh-keygen -q -f $HOME/.ssh/id_rsa -N ''
    - user: backuppc
    - onlyif: test ! -e /var/lib/backuppc/.ssh/id_rsa

#copy_pubkey:
#  file.copy:
#    - name: salt://backuppc
#    - source: /var/lib/backuppc/.ssh/id_rsa

backuppc/pubkey:
  event.send:
    - data:
      pubkey: {{salt['cmd.run']('cat /var/lib/backuppc/.ssh/id_rsa.pub')}}

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
