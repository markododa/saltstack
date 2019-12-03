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


/etc/apache2/sites-available/apache2-graphite.conf:
  file.replace:
    - pattern: 80>
    - repl: 8000>    

libapache2-mod-wsgi:
  pkg.installed

a2enmod wsgi; a2ensite apache2-graphite.conf:
  cmd.run

/etc/apache2/ports.conf:
  file.line:
    - content: Listen 8000
    - after: Listen 80$
    - mode: ensure

apache2-graphite:
  service.running:
    - enable: True
    - reload: True
    - name: apache2
    - watch:
      - pkg: install_graphite

/usr/share/icingaweb2/modules/:
  file.recurse:
      - source: salt://monitoring/files/icingaweb2-modules/

enable-module-graphite:
  cmd.run:
    - name: ln -s /usr/share/icingaweb2/modules/graphite /etc/icingaweb2/enabledModules/graphite
    - onlyif: test ! -e /etc/icingaweb2/enabledModules/graphite

/etc/icingaweb2/resources.ini:
  file.line:
    - content: charset = "latin1"
    - after: \[icinga_ido\]
    - mode: ensure

/etc/icingaweb2/modules/graphite/config.ini:
  file.managed:
    - template: jinja
    - source: salt://monitoring/files/graphite-config.ini
    - user: www-data
    - group: www-data
    - context:
        fqdn: {{salt['mine.get'](tgt='*',fun='address')['va-monitoring'][0]}}
