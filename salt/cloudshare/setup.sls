{% from "cloudshare/map.jinja" import nextcloud with context %}

install_basics:
  pkg.installed:
    - pkgs:
      - curl
      
apache2-stuff:
  pkg.installed:
    - pkgs:
      - apache2
      - php
      - php-gd
      - php-ldap
      - libapache2-mod-php
      - php-gd
      - php-json
      - php-mysql
      - php-curl
      - php-intl
      - php-mcrypt
      - php-imagick
      - php-zip
      - php-xml
      - php-mbstring

  service.running:
    - name: apache2
    - watch:
      - pkg: apache2-stuff
      - pkg: {{ nextcloud.pkg }}


install-nextcloud:
  pkg.installed:
    - name: {{ nextcloud.pkg }}
    - refresh: True

/var/www/nextcloud/config/autoconfig.php:
  file.managed:
    - source: salt://cloudshare/files/autoconfig.php
    - _mode: 644
    - user: www-data
    - group: www-data

dbname:
  file.replace:
    - name: /var/www/nextcloud/config/autoconfig.php
    - pattern: DB_NAME
    - repl: "{{ salt['pillar.get']('cloudshare_database', 'cloudshare') }}"

dbuser:
  file.replace:
    - name: /var/www/nextcloud/config/autoconfig.php
    - pattern: DB_USER
    - repl: "{{ salt['pillar.get']('cloudshare_dbuser', 'cloudshare') }}"

dbpass:
  file.replace:
    - name: /var/www/nextcloud/config/autoconfig.php
    - pattern: DB_PASS
    - repl: "{{ salt['grains.get_or_set_hash']('cloudshare_dbpass',chars='abcdefghijklmnopqrstuvwxyz0123456789', length=10) }}"

user:
  file.replace:
    - name: /var/www/nextcloud/config/autoconfig.php
    - pattern: USER
    - repl: "admin"

password:
  file.replace:
    - name: /var/www/nextcloud/config/autoconfig.php
    - pattern: PASS
    - repl: "{{ salt['pillar.get']('admin_password', '') }}"

/dev/vdb:
  blockdev.formatted:
    - onlyif:
        - test -e /dev/vdb

/mnt/va-nextcloud:
  mount.mounted:
    - device: /dev/vdb
    - fstype: ext4
    - mkmnt: True
    - onlyif:
        - test -e /dev/vdb

'mv /var/www/nextcloud /mnt/va-nextcloud/':
  cmd.run:
    - onlyif:
      - test -e /mnt/va-nextcloud
      - test ! -e /mnt/va-nextcloud/nextcloud
      - mount | grep -q /mnt/va-nextcloud

'ln -sfn /mnt/va-nextcloud/nextcloud /var/www/nextcloud':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-nextcloud/nextcloud
        - mount | grep -q /mnt/va-nextcloud

{% set multisite = salt['pillar.get']('multisite') %}

{% if multisite != True %}
/etc/apache2/sites-available/nextcloud.conf:
  file.managed:
    - source: salt://cloudshare/files/nextcloud.conf

remove_alias:
  file.replace:
    - name: /etc/apache2/sites-available/nextcloud.conf
    - pattern: Alias /nextcloud "/var/www/nextcloud/"
    - repl: Alias / "/var/www/nextcloud/"

a2ensite nextcloud:
  cmd.run


apache2:
  service.running:
    - reload: True
    - watch:
      - file: /etc/apache2/sites-available/nextcloud.conf

{% endif %}

{% set ipaddrss = salt['network.ip_addrs']()[0] %}
curl {{ipaddrss}} > /dev/null:
  cmd.run
  
/etc/sudoers.d/occ:
  file.managed:
    - source: salt://cloudshare/files/occ
    - user: root
    - group: root
    - mode: 440
    
#### functionality script
/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://cloudshare/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755
 # DA SE ISKOPIRA TEMATA VA-THEME
  
# fixredirect2contactsplus:
  # file.replace:
    # - name: /var/www/nextcloud/.htaccess
    # - pattern: /remote.php/carddav/
    # - repl: /remote.php/contactsplus/  
    
# fixredirect2calendarplus:
  # file.replace:
    # - name: /var/www/nextcloud/.htaccess
    # - pattern: /remote.php/caldav/
    # - repl: /remote.php/calendarplus/calendars/  

# sudo -u www-data php /var/www/nextcloud/occ app:disable calendar
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:disable contacts
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:disable firstrunwizard
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:disable gallery
  # cmd.run



# sudo -u www-data php /var/www/nextcloud/occ app:enable calendarplus
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable contactsplus
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable conversations
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable galleryplus
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable ocusagecharts
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable tasksplus
  # cmd.run

# sudo -u www-data php /var/www/nextcloud/occ app:enable files_share_qr
  # cmd.run
{% for app in ['tasks','calendar','contacts'] %}
sudo -u www-data php /var/www/nextcloud/occ app:install {{ app }}:
  cmd.run:
    - unless: sudo -u www-data php /var/www/nextcloud/occ app:list|grep {{ app }}
{% endfor %}

#generating sertificate/installing  
#http://codereview.stackexchange.com/questions/117956/automated-nextcloud-installation-script
