add-backports:
  pkgrepo.managed:
     - humanname: stretch backports
     - name: deb http://ftp.debian.org/debian stretch-backports main
     - file: /etc/apt/sources.list.d/backports.list

icinga_repo:
  pkgrepo.managed:
     - humanname: icinga2 repo
     - name: deb http://packages.icinga.com/debian icinga-stretch main
     - file: /etc/apt/sources.list.d/icinga2.list
     - key_url: https://packages.icinga.com/icinga.key

install_mysql:
  pkg.installed:
    - pkgs:
      - mysql-server
      - mysql-client

install_icinga2:
  pkg.installed:
    - pkgs:
      - nagios-nrpe-plugin
      - monitoring-plugins
      - icinga2
      - icinga2-ido-mysql
      - libnumber-format-perl
      - libconfig-inifiles-perl
      - libdatetime-perl
      - mailutils
      - ssmtp
      - libreadonly-xs-perl
    - require:
      - pkg: install_mysql

add-checkcommands:
    file.recurse:
        - name: /usr/lib/nagios/plugins/
        - source: salt://monitoring/files/check_cmd/
        - user: root
        - group: root
        - file_mode: 755
        - dir_mode: 755

#check permissions - down here - should not overwrite		
add-wmicpresets:
    file.recurse:
        - name: /etc/check_wmi_plus/
        - source: salt://monitoring/files/check_wmi_plus/
        - user: root
        - group: root
        - file_mode: 755
        - dir_mode: 755

add-notifications-scripts:
    file.recurse:
        - name: /etc/icinga2/scripts/
        - source: salt://monitoring/files/icinga2mail/
        - user: root
        - group: root
        - file_mode: 755
        - dir_mode: 755
        
        
/usr/bin/wmic:
  file.managed:
    - source:
      - salt://monitoring/files/wmic
    - user: root
    - group: root
    - mode: 755

#needs manual editing later, should be auto filled with credentails:	

{% set admin_pass = salt['pillar.get']('admin_pass') %}
{% set domain = salt['pillar.get']('domain') %}
{% set shortdomain = salt['pillar.get']('shortdomain') %}
{% set host_name = grains['id'] %}


/etc/ssmtp/ssmtp.conf:
  file.managed:
    - source:
      - salt://monitoring/files/ssmtp.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      MON_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      MON_HOSTNAME: {{ host_name }} 
  
  
/etc/icinga2/conf.d/cred_win_domain.txt:
  file.managed:
    - source:
      - salt://monitoring/files/cred_win_domain.txt
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      MON_SHORTDOMAIN: {{ shortdomain }}
      MON_USER: Administrator 
      MON_PASSWORD: {{ admin_pass }} 
      
icinga2-feature:
  cmd.run:
    - name: icinga2 feature enable api livestatus ido-mysql

configure-icinga2:
  file.recurse:
      - name: /etc/icinga2/conf.d/
      - source: salt://monitoring/files/icinga2

configure-template:
  file.recurse:
      - name: /etc/icinga2/zones.d/global-templates/
      - source: salt://monitoring/files/windows-templates

create-ca:
  cmd.run:
    - name: icinga2 pki new-ca
    - onlyif: test ! -e /var/lib/icinga2/ca/

/var/lib/icinga2/certs/:
  file.directory

create-cert:
  cmd.run:
    - name: chown nagios:nagios /var/lib/icinga2/certs/ && icinga2 pki new-cert --cn `hostname -f` --csr /var/lib/icinga2/certs/`hostname -f`.csr --key /var/lib/icinga2/certs/` hostname -f`.key
    - onlyif: test ! -e /var/lib/icinga2/certs/`hostname -f`.csr -a /var/lib/icinga2/certs/`hostname -f`.key

create-crt:
  cmd.run:
    - name: icinga2 pki sign-csr --csr /var/lib/icinga2/certs/`hostname -f`.csr --cert /var/lib/icinga2/certs/`hostname -f`.crt
    - onlyif: test ! -e /var/lib/icinga2/certs/`hostname -f`.crt

cp /var/lib/icinga2/ca/ca.crt /var/lib/icinga2/certs/ && chown nagios:nagios /var/lib/icinga2/certs/ca.crt && service icinga2 stop:
  cmd.run:
  - onlyif: test ! -e /var/lib/icinga2/certs/ca.crt

#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True


check_functionality_monitoring:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://monitoring/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

restart_functionality_monitoring:
  file.managed:
    - name: /usr/lib/nagios/plugins/restart_functionality.sh
    - source: salt://monitoring/files/restart_functionality.sh
    - user: root
    - group: root
    - mode: 755

/etc/icinga2/conf.d/templates.conf:
  file.line:
    - content: '  enable_flapping = true'
    - after: template Host "generic-host" {
    - mode: ensure
    
/etc/icinga2/conf.d/templates.conf:
  file.line:
    - content: '  enable_flapping = true'
    - after: template Service "generic-service" {
    - mode: ensure

{% for service in ['mail-host-notification', 'mail-service-notification'] %}
{{ service }}:
  file.line:
    - name: /etc/icinga2/conf.d/notifications.conf
    - content: '  interval = 0'
    - after: {{ service }}
    - mode: ensure
{% endfor %}

icinga2:
  service.running:
    - reload: True
  
#Weekly report cron job   
/etc/icinga2/scripts/mail-report.sh:
  cron.present:
    - user: root
    - minute: 0
    - hour: 8
    - dayweek: 1

/opt/va/icinga2/va-host.tmpl:
  file.managed:
    - source: salt://monitoring/files/va_host.conf
    - makedirs: True
