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
    - source: salt://files/rra.cfg

npcd:
  service.running: []
