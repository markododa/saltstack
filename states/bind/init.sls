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
        top_level_domain: {{ salt['pillar.get']('top_level_domain') }}
        ip: {{ salt['pillar.get']('zone_bind_ip') }}
        port: {{ salt['pillar.get']('zone_bind_port') }}

bind9:
  service.running:
    - restart: True
    - watch:
      - file: /etc/bind/named.conf.local
