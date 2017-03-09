add-backports:
  pkgrepo.managed:
    - humanname: cyconet jessie backports
    - name: deb     http://ftp.cyconet.org/debian jessie-backports     main non-free contrib
    - file: /etc/apt/sources.list.d/backports-cyconet.list
    - key_url: http://ftp.cyconet.org/debian/repo.key

add_restricted:
  pkgrepo.managed:
    - humanname: cyconet restricted
    - name: deb     http://ftp.cyconet.org/debian restricted main non-free contrib
    - file: /etc/apt/sources.list.d/restricted-cyconet.list
    - key_url: http://ftp.cyconet.org/debian/repo.key

install_pnp4nagios:
  pkg.installed:
    - pkgs:
      - debian-cyconet-archive-keyring
      - pnp4nagios
      - rrdcached
      - python-rrdtool

/etc/default/npcd:
  file.replace:
    - pattern: RUN="no"
    - repl: RUN="yes"

/etc/pnp4nagios/npcd.cfg:
  file.replace:
    - pattern: perfdata_spool_dir = /var/spool/pnp4nagios/npcd/
    - repl: perfdata_spool_dir = /var/spool/icinga2/perfdata

/etc/pnp4nagios/rra.cfg:
  file.managed:
    - source: salt://monitoring/files/rra.cfg


pnp4nagios_pass:
  cmd.run:
    - name: htpasswd -b -c /etc/pnp4nagios/htpasswd.users admin {{ salt['pillar.get']('admin_password') }}

{% for line in ['^.*AuthName "Icinga Access"','^.*AuthType Basic','^.*AuthUserFile .*','Require valid-user'] %}
{{ line }}:
  file.comment:
    - name: /etc/apache2/conf-available/pnp4nagios.conf
    - regex: {{ line }}
{% endfor %}
      

icinga_restart:
  pkg.installed:
    - name: icinga2
    - service.running:
      - name: icinga2
      - watch:
        - pkg: pnp4nagios

npcd_restart:
  pkg.installed:
    - name: pnp4nagios
    - service.running:
      - name: npcd
      - watch:
        - pkg: pnp4nagios
