install_ticketing_phase1:
  pkg.installed:
    - pkgs:
      - imagemagick
      - apache2
      - libapache2-mod-passenger
      - mysql-server
      - mysql-client 
      - ruby-dev 
      - gcc
      - libmysqlclient-dev
      - libpq-dev
      - libsqlite3-dev
      - libev-dev 

{% set ticketing_password = salt['pillar.get']('redmine_password') %}


redmine-db1:
  cmd.run:
    - name: echo "CREATE DATABASE redmine character SET utf8; CREATE user 'redmine'@'localhost' IDENTIFIED BY 'redmine'; GRANT ALL privileges ON redmine.* TO 'redmine'@'localhost'; set password for 'redmine'@'localhost'= password('{{ ticketing_password }}');flush privileges;" | mysql -uroot
    - unless: echo 'show databases;' | mysql -uroot | grep -q redmine


/etc/dbconfig-common/redmine/instances/default.conf:
  file.managed:
    - source: salt://ticketing/files/default.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      REDMINE_PASS: {{ ticketing_password }}
    - makedirs: True

/usr/share/redmine/templates/database-mysql2.yml.template:
  file.managed:
    - source: salt://ticketing/files/database-mysql2.yml.template
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      REDMINE_PASS: {{ ticketing_password }}
    - makedirs: True

install_ticketing_phase2:
  pkg.installed:
    - pkgs:
      - redmine
      - redmine-mysql

update_gems:
  cmd.run:
    - name: gem update  --no-ri --no-rdoc

install_bundler:
  cmd.run:
    - name: gem install bundler --no-ri --no-rdoc

/etc/apache2/mods-available/passenger.conf:
  file.managed:
    - source: salt://ticketing/files/passenger.conf
    - user: root
    - group: root
    - mode: 644

stop_apache2:
  service.dead:
    - name: apache2

/var/www/html/redmine:
  file.symlink:
    - target: /usr/share/redmine/public
    - force: True

/etc/apache2/sites-available/000-default.conf:
  file.managed:
    - source: salt://ticketing/files/000-default.conf
    - user: root
    - group: root
    - mode: 644

/usr/share/redmine/Gemfile.lock:
  file.managed:
    - source: salt://ticketing/files/Gemfile.lock
    - user: www-data
    - group: www-data
    - mode: 644

/usr/share/redmine/config/settings.yml:
  file.managed:
    - source: salt://ticketing/files/settings.yml
    - user: root
    - group: root
    - mode: 644

theme-redmine:
    file.recurse:
        - name: /usr/share/redmine/public/themes/gitmake
        - source: salt://ticketing/files/gitmake
        - clean: True
        - include_empty: True

apache2:
  service.running:
    - enable: True

/usr/share/redmine/tmp/restart.txt:
  file.managed:
    - source: salt://ticketing/files/Gemfile.lock
    - user: root
    - group: root
    - mode: 644


#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True

check_functionality_ticketing:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://ticketing/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

