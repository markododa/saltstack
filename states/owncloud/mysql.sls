include:
  - owncloud.python-mysqldb

mysql-requirements:
  pkg.installed:
    - pkgs:
      - mysql-server
      - mysql-client
    - require_in:
      - service: mysql
      - mysql_user: {{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}

mysql:
  service.running:
    - watch:
      - pkg: mysql-requirements

owncloud-local:
  mysql_user.present:
    - name: {{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}
    - host: localhost
    - password: {{ salt['grains.get_or_set_hash']('owncloud_dbpass',chars='abcdefghijklmnopqrstuvwxyz0123456789', length=10) }}
    - require:
      - pkg: python-mysqldb
      - pkg: mysql-requirements
      - service: mysql

ownclouddb:
  mysql_database.present:
    - name: {{ salt['pillar.get']('owncloud_database', 'owncloud') }}
    - require:
      - mysql_user: {{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}
      - pkg: python-mysqldb
  mysql_grants.present:
    - grant: all privileges
    - database:  {{ salt['pillar.get']('owncloud_database', 'owncloud') }}.*
    - host: localhost
    - user: {{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}
    - require:
      - mysql_database: {{ salt['pillar.get']('owncloud_database', 'owncloud') }}
      - pkg: python-mysqldb
      - service: mysql
