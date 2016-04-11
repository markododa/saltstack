{% from "owncloud/map.jinja" import owncloud with context %}

apache2-stuff:
  pkg.installed:
    - pkgs:
      - apache2
      - php5
      - php5-gd
  service.running:
    - name: apache2
    - watch:
      - pkg: apache2-stuff
      - pkg: {{ owncloud.pkg }}


install-owncloud:
  pkg.installed:
    - name: {{ owncloud.pkg }}
    - refresh: True

/var/www/owncloud/config/autoconfig.php:
  file.managed:
    - source: salt://owncloud/files/autoconfig.php
    - file_mode: 644
    - user: www-data
    - group: www-data

dbname:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: DB_NAME
    - repl: "{{ salt['pillar.get']('owncloud_database', 'owncloud') }}"

dbuser:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: DB_USER
    - repl: "{{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}"

dbpass:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: DB_PASS
    - repl: "{{ salt['grains.get_or_set_hash']('owncloud_dbpass',chars='abcdefghijklmnopqrstuvwxyz0123456789', length=10) }}"

user:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: USER
    - repl: "admin"

password:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: PASS
    - repl: "{{ salt['pillar.get']('admin_password', '') }}"

/dev/vdb:
  blockdev.formatted

/mnt/va-owncloud:
  mount.mounted:
    - device: /dev/vdb
    - fstype: ext4
    - mkmnt: True

'mv /var/www/owncloud /mnt/va-owncloud/':
  cmd.run:
    - unless: test -e /mnt/va-owncloud/owncloud

/var/www/owncloud:
  file.symlink:
    - target: /mnt/va-owncloud/owncloud

{% set multisite = salt['pillar.get']('multisite') %}

{% if multisite != True %}
remove_alias:
  file.replace:
    - name: /etc/apache2/conf-available/owncloud.conf
    - pattern: Alias /owncloud "/var/www/owncloud/"
    - repl: Alias / "/var/www/owncloud/"

apache2:
  service.running:
    - reload: True
    - watch:
      - file: /etc/apache2/conf-available/owncloud.conf

{% endif %}

{% set ipaddrss = salt['network.ip_addrs']()[0] %}
curl {{ipaddrss}} > /dev/null:
  cmd.run
