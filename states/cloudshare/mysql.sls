include:
  - cloudshare.python-mysqldb

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

mysql -uroot --execute "GRANT ALL PRIVILEGES ON owncloud.* TO 'owncloud'@'localhost';":
  cmd.run

grant_all_on_db:
  mysql_grants.present:
    - grant: ALL PRIVILEGES
    - database: 'owncloud.*'
    - host: localhost
    - user: {{ salt['pillar.get']('owncloud_dbuser', 'owncloud') }}
    - require:
      - pkg: python-mysqldb
