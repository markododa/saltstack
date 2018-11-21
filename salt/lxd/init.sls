snapd:
  pkg.installed

snap install lxd:
  cmd.run

/opt/lxd-preseed:
  file.managed:
    - template: jinja
    - source: salt://lxd/preseed
    - context:
        trust_password: {{salt['pillar.get']('admin_password')}}

source /etc/profile; cat /opt/lxd-preseed| lxd init --preseed:
  cmd.run

source /etc/profile; lxc profile set default security.privileged true:
  cmd.run
