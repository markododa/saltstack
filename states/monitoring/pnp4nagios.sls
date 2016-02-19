add-backports:
  pkgrepo.managed:
    - humanname: cyconet jessie backports
    - name: deb     http://ftp.cyconet.org/debian jessie-backports     main non-free contrib
    - file: /etc/apt/sources.list.d/backports-cyconet.list
    - key_url: http://ftp.cyconet.org/debian/repo.key

install_pnp4nagios:
  pkg.installed:
    - pkgs:
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

/etc/apache2/conf-available/pnp4nagios.conf:
  file.replace:
    - pattern: /etc/icinga/htpasswd.users
    - repl: /etc/pnp4nagios/htpasswd.users

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
