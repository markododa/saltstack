wget -q https://releases.hashicorp.com/consul/0.7.4/consul_0.7.4_linux_amd64.zip:
  cmd.run:
    - creates: /root/consul_0.7.4_linux_amd64.zip

/usr/bin:
  archive.extracted:
    - source: /root/consul_0.7.4_linux_amd64.zip
    - enforce_toplevel: False

/etc/systemd/system/consul.service:
  file.managed:
    - source: salt://va-master/consul.service
