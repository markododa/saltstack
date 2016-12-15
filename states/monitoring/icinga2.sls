{% if grains['os'] == 'Debian' %}
debmon_repo_required_packages:
  pkg.installed:
    - name: python-apt

icinga_repo:
  pkgrepo.managed:
    - humanname: debmon
    - name: deb http://debmon.org/debmon debmon-jessie main
    - file: /etc/apt/sources.list.d/debmon.list
    - key_url: http://debmon.org/debmon/repo.key
    - require:
      - pkg: debmon_repo_required_packages


{% elif grains['os'] == 'Ubuntu' %}

icinga_repo:
  pkgrepo.managed:
    - ppa: formorer/icinga


{% endif %}

install_icinga2:
  pkg.installed:
    - pkgs:
      - icinga2
      - mysql-server
      - mysql-client
      - icinga2-ido-mysql

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
        - name: /ets/check_wmi_plus/
        - source: salt://monitoring/files/check_wmi_plus/
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

icinga2:
  service.running: []
