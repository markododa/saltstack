include:
  - monitoring.icinga2
  - monitoring.graphite

install_icingaweb2:
  pkg.installed:
    - pkgs:
      - apache2
      - icingaweb2
      - php-intl
      - php-imagick

icingaweb2-feature:
  cmd.run:
    - name: icinga2 feature enable command
  service.running:
    - name: icinga2
    - restart: True

time_zone:
  cmd.run:
    - name: sed -i '/;date.timezone =/ a\date.timezone = "Europe/Skopje"' /etc/php/7.0/apache2/php.ini

{% set dbpass = salt['grains.get_or_set_hash']('icingaweb2dbpass',chars='abcdefghijklmnopqrstuvwxyz0123456789', length=10) %}

icingaweb2-db:
  cmd.run:
    - name: echo "CREATE DATABASE icingaweb2; GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE VIEW, INDEX, EXECUTE ON icingaweb2.* TO 'icingaweb2'@'localhost' IDENTIFIED BY '{{ dbpass }}';" | mysql -uroot
    - unless: echo 'show databases;' | mysql -uroot |grep -q icingaweb2

icingaweb-db-populate:
  cmd.run:
    - name: mysql -uroot icingaweb2 < /usr/share/icingaweb2/etc/schema/mysql.schema.sql
    - unless: echo 'show tables;' | mysql -uroot icingaweb2 |grep -q icingaweb_user

icinga2web-autoconfigure:
    file.recurse:
        - name: /etc/icingaweb2
        - source: salt://monitoring/files/icingaweb2/
        - makedirs: True
        - user: www-data
        - group: icingaweb2
        - dir_mode: 750
        - file_mode: 644
        - include_empty: True

/etc/icingaweb2/enabledModules/:
  file.directory:
    - makedirs: True
    - user: www-data
    - group: icingaweb2
    - makedirs: True
    - dir_mode: 750

enable-module-monitoring:
  cmd.run:
    - name: ln -s /usr/share/icingaweb2/modules/monitoring /etc/icingaweb2/enabledModules/monitoring
    - onlyif: test ! -e /etc/icingaweb2/enabledModules/monitoring

enable-module-pnp:
  cmd.run:
    - name: ln -s /etc/icingaweb2/modules/pnp/ /etc/icingaweb2/enabledModules/pnp
    - onlyif: test ! -d /etc/icingaweb2/enabledModules/pnp

ido-pass:
  cmd.run:
    - name: sed -i "s#IDODBPASS#\"`awk -F= '/dbc_dbpass=/{print substr($2,2, length($2)-2) }' /etc/dbconfig-common/icinga2-ido-mysql.conf`\"#" /etc/icingaweb2/resources.ini

ido-user:
  cmd.run:
    - name: sed -i "s#IDODBUSER#\"`awk -F= '/dbc_dbuser=/{print substr($2,2, length($2)-2) }' /etc/dbconfig-common/icinga2-ido-mysql.conf`\"#" /etc/icingaweb2/resources.ini

ido-dbname:
  cmd.run:
    - name: sed -i "s#IDODBNAME#\"`awk -F= '/dbc_dbname=/{print substr($2,2, length($2)-2) }' /etc/dbconfig-common/icinga2-ido-mysql.conf`\"#" /etc/icingaweb2/resources.ini

icingaweb2-pass:
    file.replace:
    - name: /etc/icingaweb2/resources.ini
    - pattern: ICINGAWEB2DBPASS
    - repl: {{ dbpass }}

admin-user:
  cmd.run:
    - name: echo "INSERT INTO icingaweb_user (name, active, password_hash) VALUES ('admin', 1, '$(openssl passwd -1 {{ salt['pillar.get']('admin_password') }})' );" | mysql -u icingaweb2 -p{{ dbpass }} icingaweb2
    - unless: echo 'SELECT * FROM icingaweb_user;' | mysql -uroot icingaweb2 |grep -q admin

'rm /etc/apache2/sites-enabled/000-default.conf':
  cmd.run:
    - onlyif: test -e /etc/apache2/sites-enabled/000-default.conf

{% set multisite = salt['pillar.get']('multisite') %}

{% if multisite != True %}
remove_alias:
  file.replace:
    - name: /etc/apache2/conf-available/icingaweb2.conf
    - pattern: Alias /icingaweb2 "/usr/share/icingaweb2/public"
    - repl: DocumentRoot /usr/share/icingaweb2/public

remove_rewrite:
  file.replace:
    - name: /etc/apache2/conf-available/icingaweb2.conf
    - pattern: RewriteBase /icingaweb2/
    - repl: RewriteBase /

apache2:
  service.running:
    - reload: True
    - watch:
      - file: /etc/apache2/conf-available/icingaweb2.conf

{% endif %}

salt/app/new:
  event.send:
    - data:
        sls: base.nrpe
