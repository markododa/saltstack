{% set data = data['data'] %}

{% if data['type'] == 'monitoring' %}
{% set folders = ['/etc/icinga2', '/root/.va/backup', '/etc/ssmtp', '/usr/lib/nagios/plugins',  '/var/lib/pnp4nagios/perfdata/', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'directory' %}
{% set folders = ['/root/.va/backup', '/etc/openvpn', '/etc/samba', '/var/lib/samba/', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'backup' %}
{% set folders = ['/etc/backuppc', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'cloudshare' %}
{% set folders = ['/root/.va/backup', '/var/www/owncloud', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'fileshare' %}
{% set folders = ['/home', '/etc/samba', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'email' %}
{% set folders = ['/etc/postfix', '/root/.va/backup', '/var/vmail/', '/etc/nagios/nrpe.d/'] %}
{% elif data['type'] == 'proxy' %}
{% set folders = [''/root/.va/backup', '/etc/lighttpd/', '/etc/squid/', '/var/www/html/', '/etc/e2guardian/', '/usr/share/e2guardian/', '/etc/nagios/nrpe.d/'] %}
{% else %}
{% set folders = ['/root/.va/backup'] %}
{% endif %}

add_host_to_backup:
  local.va_backup.add_rsync_host:
    - tgt: 'role:backup'
    - expr_form: grain
    - args:
      - hostname: {{ data['fqdn'] }}
      - address: {{ data['ip'] }}

add_folders_to_backup:
  local.va_backup.add_folder_list:
    - tgt: 'role:backup'
    - expr_form: grain
    - args:
      - hostname: {{ data['fqdn'] }}
      - folder_list: {{ folders }}
