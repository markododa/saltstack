install_mysql:
  pkg.installed:
    - pkgs:
      - mysql-server
      - mysql-client

install_icinga2:
  pkg.installed:
    - pkgs:
      - nagios-nrpe-plugin
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
    - name: icinga2 feature enable api livestatus perfdata ido-mysql

configure-icinga2:
  file.recurse:
      - name: /etc/icinga2/conf.d/
      - source: salt://monitoring/files/icinga2

create-ca:
  cmd.run:
    - name: icinga2 pki new-ca
    - onlyif: test ! -e /var/lib/icinga2/ca/

create-cert:
  cmd.run:
    - name: chown nagios:nagios /etc/icinga2/pki/ && icinga2 pki new-cert --cn `hostname -f` --csr /etc/icinga2/pki/`hostname -f`.csr --key /etc/icinga2/pki/` hostname -f`.key
    - onlyif: test ! -e /etc/icinga2/pki/`hostname -f`.csr -a /etc/icinga2/pki/`hostname -f`.key

create-crt:
  cmd.run:
    - name: icinga2 pki sign-csr --csr /etc/icinga2/pki/`hostname -f`.csr --cert /etc/icinga2/pki/`hostname -f`.crt
    - onlyif: test ! -e /etc/icinga2/pki/`hostname -f`.crt

cp /var/lib/icinga2/ca/ca.crt /etc/icinga2/pki/ && chown nagios:nagios /etc/icinga2/pki/ca.crt && service icinga2 stop:
  cmd.run:
  - onlyif: test ! -e /etc/icinga2/pki/ca.crt

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

icinga2:
  service.running: []
  
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