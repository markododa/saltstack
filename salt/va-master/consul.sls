wget -q https://releases.hashicorp.com/consul/1.4.3/consul_1.4.3_linux_amd64.zip:
  cmd.run:
    - creates: /root/consul_1.4.3_linux_amd64.zip

/usr/bin:
  archive.extracted:
    - source: /root/consul_1.4.3_linux_amd64.zip
    - enforce_toplevel: False

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

consul:
  service.running:
    - enable: True
    - restart: True
    - watch:
      - file: /etc/consul.d/consul.json
