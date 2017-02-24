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

/etc/nagios/nrpe.d/va.cfg:
  file.managed:
    - source:
      - salt://base/files/nrpe/va.cfg
    - user: root
    - group: root
    - mode: 644

{% if "va-monitoring" in salt['mine.get'](tgt='role:va-master',fun='address',expr_form='grain') %}

/etc/nagios/nrpe.cfg:
  file.replace:
    - pattern: 'allowed_hosts=127.0.0.1'
    - repl: 'allowed_hosts={{salt['mine.get'](tgt='role:va-master',fun='address',expr_form='grain')['va-monitoring'][0]}}'

nagios-nrpe-server:
  service.running:
  - watch:
    - file: /etc/nagios/nrpe.cfg

{% endif %}

salt/nrpe-agent/installed:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{salt['network.ip_addrs']()[-1] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['fqdn'] }}
    - order: last

dummy_check_functionality:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source:
      - salt://base/files/nrpe/check_functionality.sh
    - user: root
    - group: root
    - mode: 755
    - replace: False
