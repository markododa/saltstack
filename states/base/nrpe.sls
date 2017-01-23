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

/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://base/files/nrpe/check_functionality.sh
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
    - repl: 'allowed_hosts={{salt['mine.get'](tgt='role:monitoring',fun='inventory',expr_form='grain')['va-monitoring']['ip4_interfaces']['eth0'][0]}}'

nagios-nrpe-server:
  service.running:
  - watch:
    - file: /etc/nagios/nrpe.cfg

salt/nrpe-agent/installed:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{salt['network.ip_addrs']()[-1] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['fqdn'] }}
    - order: last
