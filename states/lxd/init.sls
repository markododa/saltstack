snapd:
  pkg.installed

snap install lxd:
  cmd.run

lxc profile set default security.privileged true:
  cmd.run
