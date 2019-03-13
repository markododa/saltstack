install_consul_pkgs:
  pkg.installed:
    - pkgs:
      - wget
      - unzip

wget -q https://releases.hashicorp.com/consul/1.4.3/consul_1.4.3_linux_amd64.zip:
  cmd.run:
    - creates: /root/consul_1.4.3_linux_amd64.zip
    - require:
      - pkg: install_consul_pkgs

/usr/bin:
  archive.extracted:
    - source: /root/consul_1.4.3_linux_amd64.zip
    - enforce_toplevel: False
    - require:
      - pkg: install_consul_pkgs

/etc/consul.d:
  file.directory

/etc/consul.d/consul.json:
  file.managed:
    - source: salt://va-master/consul.json

/etc/systemd/system/consul.service:
  file.managed:
    - source: salt://va-master/consul.service

mv /usr/share/consul /var/lib/:
  cmd.run:
    - unless: test -d /var/lib/consul
    - onlyif: test -d /usr/share/consul

systemctl enable consul --now:
 cmd.run:
      - unless: test -f  /.dockerenv
