include:
  - cloudshare.python-mysqldb

mysql-requirements:
  pkg.installed:
    - pkgs:
      - mysql-server
      - mysql-client
    - require_in:
      - service: mysql
      - mysql_user: {{ salt['pillar.get']('cloudshare_dbuser', 'cloudshare') }}

mysql:
  service.running:
    - watch:
      - pkg: mysql-requirements

cloudshare-local:
  mysql_user.present:
    - name: {{ salt['pillar.get']('cloudshare_dbuser', 'cloudshare') }}
    - host: localhost
    - password: {{ salt['grains.get_or_set_hash']('cloudshare_dbpass',chars='abcdefghijklmnopqrstuvwxyz0123456789', length=10) }}
    - require:
      - pkg: python-mysqldb
      - pkg: mysql-requirements
      - service: mysql

cloudsharedb:
  mysql_database.present:
    - name: {{ salt['pillar.get']('cloudshare_database', 'cloudshare') }}
    - require:
      - mysql_user: {{ salt['pillar.get']('cloudshare_dbuser', 'cloudshare') }}
      - pkg: python-mysqldb

mysql -uroot --execute "GRANT ALL PRIVILEGES ON cloudshare.* TO 'cloudshare'@'localhost';":
  cmd.run

grant_all_on_db:
  mysql_grants.present:
    - grant: ALL PRIVILEGES
    - database: 'cloudshare.*'
    - host: localhost
    - user: {{ salt['pillar.get']('cloudshare_dbuser', 'cloudshare') }}
    - require:
      - pkg: python-mysqldb
