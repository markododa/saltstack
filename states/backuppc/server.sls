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

