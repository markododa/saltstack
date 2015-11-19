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
      - nagios-nrpe-plugin
      - icinga2
      - mysql-server
      - mysql-client
      - icinga2-ido-mysql

icinga2-feature:
  cmd.run:
    - name: icinga2 feature enable api icingastatus livestatus perfdata ido-mysql

configure-icinga2:
    file.recurse:
        - name: /etc/icinga2/conf.d/
        - source: salt://monitoring/files/icinga2

create-ca:
  cmd.run:
    - name: icinga2 pki new-ca
    - onlyif: test ! -e /var/lib/icinga2/ca/

{% set hostname = salt['cmd.run']('hostname -f') %}

create-cert:
  cmd.run:
    - name: chown nagios:nagios /etc/icinga2/pki/ && icinga2 pki new-cert --cn {{ hostname }} --csr /etc/icinga2/pki/{{ hostname }}.csr --key /etc/icinga2/pki/{{ hostname }}.key
    - onlyif: test ! -e /etc/icinga2/pki/{{ hostname }}.csr -a /etc/icinga2/pki/{{ hostname }}.key

create-crt:
  cmd.run:
    - name: icinga2 pki sign-csr --csr /etc/icinga2/pki/{{ hostname }}.csr --cert /etc/icinga2/pki/{{ hostname }}.crt
    - onlyif: test ! -e /etc/icinga2/pki/{{ hostname }}.crt

cp /var/lib/icinga2/ca/ca.crt /etc/icinga2/pki/ && chown nagios:nagios /etc/icinga2/pki/ca.crt && service icinga2 stop:
  cmd.run:
  - onlyif: test ! -e /etc/icinga2/pki/ca.crt

icinga2:
  service.running: []
