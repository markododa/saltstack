snapd:
  pkg.installed

snap install lxd:
  cmd.run

/opt/lxd-preseed:
  file.managed:
    - source: salt://lxd/preseed

cat /opt/lxd-preseed| lxd init --preseed:
  cmd.run

source /etc/profile; lxc profile set default security.privileged true:
  cmd.run
