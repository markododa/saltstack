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

default_va_cfg:
  file.managed:
    - source: salt://base/files/nrpe/va.cfg
    - name: /etc/nagios/nrpe.d/va.cfg
    - user: root
    - group: root
    - mode: 644
    - replace: False 

{% if "va-monitoring" in salt['mine.get'](tgt='*',fun='address') %}

/etc/nagios/nrpe.cfg:
  file.replace:
    - pattern: 'allowed_hosts=127.0.0.1'
    - repl: 'allowed_hosts={{salt['mine.get'](tgt='*',fun='address')['va-monitoring'][0]}}'

timeout:
  file.replace:
    - name: /etc/nagios/nrpe.cfg
    - pattern: 'command_timeout=60'
    - repl: 'command_timeout=250'
    
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
