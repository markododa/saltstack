# echo "mysql-server-5.5 mysql-server/root_password password root" | debconf-set-selections
# echo "mysql-server-5.5 mysql-server/root_password_again password root" | debconf-set-selections
# apt-get -y install mysql-server-5.5
# https://www.digitalocean.com/community/tutorials/saltstack-infrastructure-creating-salt-states-for-mysql-database-servers
# https://www.howtoforge.com/ubuntu_lamp_for_newbies
# https://docs.saltstack.com/en/latest/topics/tutorials/states_pt1.html
# https://help.ubuntu.com/community/ApacheMySQLPHP
# https://www.linode.com/docs/applications/salt/salt-states-configuration-apache-mysql-php

apache2-stuff:
  pkg.installed:
    - pkgs:
      - apache2
      - php5-mysql
      - libapache2-mod-php5
      - libapache2-mod-aut-mysql
  service.running:
      - enable: True
      - name: apache2
      - watch:
      - pkg: apache2-stuff

/var/www/html/index.html:     
  file.managed:          
    - source: salt://lamp/index.html
    - user: root
    - group: root
    - mode: 644

/etc/apache2/apache2.conf:
  file.managed:
    - source: salt://lamp/http.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        custom_var: "override"
    - defaults:
        custom_var: "default value"
        other_var: 123

debconf-utils:
  pkg.installed

mysql_setup:
  debconf.set:
    - name: mysql-server
    - data:
        'mysql-server/root_password': {'type': 'password', 'value': '{{ salt['pillar.get']('mysql_root_pw', '') }}' }
        'mysql-server/root_password_again': {'type': 'password', 'value': '{{ salt['pillar.get']('mysql_root_pw', '') }}' }
    - require:
      - pkg: debconf-utils

python-mysqldb:
  pkg.installed

mysql-server:
  pkg.installed:
    - require:
      - debconf: mysql-server
      - pkg: python-mysqldb

mysql:
  service.running:
    - watch:
      - pkg: mysql-server
      - file: /etc/mysql/my.cnf


# /etc/mysql/my.cnf:
  # file.managed:
    # - source: salt://mysql/files/etc/mysql/my.cnf.jinja
    # - template: jinja
    # - user: root
    # - group: root
    # - mode: 640
    # - require:
      # - pkg: mysql-server

# /etc/salt/minion.d/mysql.conf:
  # file.managed:
    # - source: salt://mysql/files/etc/salt/minion.d/mysql.conf
    # - user: root
    # - group: root
    # - mode: 640
    # - require:
      # - service: mysql

# /etc/mysql/salt.cnf:
  # file.managed:
    # - source: salt://mysql/files/etc/mysql/salt.cnf.jinja
    # - template: jinja
    # - user: root
    # - group: root
    # - mode: 640
    # - require:
      # - service: mysql

# restart_minion_for_mysql:
  # service.running:
    # - name: salt-minion
    # - watch:
      # - file: /etc/salt/minion.d/mysql.conf
