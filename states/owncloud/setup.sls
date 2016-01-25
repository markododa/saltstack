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
    - repl: "{{ salt['pillar.get']('owncloud_database', '') }}"

dbuser:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: DB_USER
    - repl: "{{ salt['pillar.get']('owncloud_dbuser', '') }}"

dbpass:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: DB_PASS
    - repl: "{{ salt['pillar.get']('owncloud_dbpass', '') }}"

user:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: USER
    - repl: "{{ salt['pillar.get']('owncloud_user', '') }}"

password:
  file.replace:
    - name: /var/www/owncloud/config/autoconfig.php
    - pattern: PASS
    - repl: "{{ salt['pillar.get']('owncloud_password', '') }}"
