bind_pkgs:
  pkg.installed:
    - pkgs:
      - bind9
      - bind9utils

/etc/default/bind9:
  file.replace:
    - pattern: OPTIONS="-u bind"
    - repl: OPTIONS="-4 -u bind"

/etc/bind/named.conf.local:
  file.append:
    - source: salt://bind/zone
    - template: jinja
    - context:
        top_level_domain: "va"

bind9:
  service.running:
    - restart: True
    - watch:
      - file: /etc/bind/named.conf.local
