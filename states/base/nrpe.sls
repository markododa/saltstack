install_nrpe:
  pkg.installed:
    - pkgs:
      - nagios-nrpe-server
      - libsys-statistics-linux-perl

/usr/lib/nagios/plugins/check_linux_stats.pl:
  file.managed:
    - source:
      - salt://base/files/nrpe/check_linux_stats.pl
    - user: root
    - group: root
    - mode: 755

/usr/lib/nagios/plugins/check_snmp_int.pl:
  file.managed:
    - source:
      - salt://base/files/nrpe/check_snmp_int.pl
    - user: root
    - group: root
    - mode: 755


/etc/nagios/nrpe.d/va.cfg:
  file.managed:
    - source:
      - salt://base/files/nrpe/va.cfg
    - user: root
    - group: root
    - mode: 644

/etc/nagios/nrpe.cfg:
  file.replace:
    - pattern: 'allowed_hosts=127.0.0.1'
    - repl: 'allowed_hosts={{ salt['grains.get']('master') }}'

nagios-nrpe-server:
  service.running:
  - watch:
    - file: /etc/nagios/nrpe.cfg

salt/nrpe-agent/installed:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{ grains['ip4_interfaces']['eth0'][0] }}
        type: {{ grains['role'] }}
