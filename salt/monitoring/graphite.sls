add-backports:
  pkgrepo.managed:
     - humanname: jessie backports
     - name: deb http://ftp.debian.org/debian stretch-backports main
     - file: /etc/apt/sources.list.d/backports.list

apt install -t stretch-backports icingaweb2:
  cmd.run

install_graphite:
  pkg.installed:
    - pkgs:
      - graphite-carbon
      - graphite-web
    - fromrepo: "stretch-backports"

icinga2 feature enable graphite:
  cmd.run

graphite-manage migrate --settings=graphite.settings --run-syncdb:
  cmd.run

chown -R _graphite:_graphite /var/lib/graphite/graphite.db /var/log/graphite:
  cmd.run

cp /usr/share/graphite-web/apache2-graphite.conf /etc/apache2/sites-available/:
  cmd.run:
    - unless: test -e /etc/apache2/sites-available/apache2-graphite.conf

libapache2-mod-wsgi:
  pkg.installed

a2enmod wsgi; a2ensite apache2-graphite.conf:
  cmd.run

/etc/apache2/ports.conf:
  file.line:
    - content: Listen 8000
    - after: Listen 80$
    - mode: ensure

apache2:
  service.running:
    - enable: True
    - reload: True
    - watch:
      - pkg: install_graphite

/usr/share/icingaweb2/modules/:
  file.recurse:
      - source: salt://monitoring/files/icingaweb2-modules/

enable-module-monitoring:
  cmd.run:
    - name: ln -s /usr/share/icingaweb2/modules/graphite /etc/icingaweb2/enabledModules/graphite
    - onlyif: test ! -e /etc/icingaweb2/enabledModules/graphite

/etc/icingaweb2/resources.ini:
  file.line:
    - content: charset = "latin1"
    - after: \[icinga_ido\]
    - mode: ensure
