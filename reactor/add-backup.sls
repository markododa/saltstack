{% set data = data['data'] %}

{% if data['type'] == 'monitoring' %}
{% set folders = ['/etc/icinga2','/root/.va/backup','/var/lib/pnp4nagios/perfdata/'] %}
{% elif data['type'] == 'directory' %}
{% set folders = ['/etc/openvpn','/root/.va/backup'] %}
{% elif data['type'] == 'backup' %}
{% set folders = ['/etc/backuppc'] %}
{% elif data['type'] == 'owncloud' %}
{% set folders = ['/var/www/owncloud','/root/.va/backup'] %}
{% elif data['type'] == 'fileshare' %}
{% set folders = ['/home','/etc/samba'] %}
{% elif data['type'] == 'email' %}
{% set folders = ['/etc','/root/.va/backup','/var/vmail'] %}
{% else %}
{% set folders = ['/root/.va/backup'] %}
{% endif %}

add_folders_to_backup:
  local.backuppc.add_folder_list:
    - tgt: 'role:backup'
    - expr_form: grain
    - arg:
      - {{ data['fqdn'] }} 
      - {{ folders }}
