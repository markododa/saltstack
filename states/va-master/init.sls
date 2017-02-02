salt://va-master/node-repo.sh:
  cmd.script:
    - onlyif: test ! -e /etc/apt/sources.list.d/nodesource.list

install_pkgs:
  pkg.installed:
    - pkgs:
      - build-essential
      - python-dev
      - libssl-dev
      - libffi-dev
      - libzmq-dev
      - unzip
      - supervisor
      - curl
      - python-libvirt
      - nodejs
      - python-setuptools
      - salt-master
      - salt-cloud
      - git

easy_install pip:
  cmd.run

wget -q https://releases.hashicorp.com/consul/0.7.0/consul_0.7.0_linux_amd64.zip:
  cmd.run:
    - creates: /root/consul_0.7.0_linux_amd64.zip

/usr/bin:
  archive.extracted:
    - source: /root/consul_0.7.0_linux_amd64.zip
    - enforce_toplevel: False

/etc/systemd/system/consul.service:
  file.managed:
    - source: salt://va-master/consul.service

consul:
  service.running:
    - enable: True 

va_master:
  git.latest:
    - name: https://github.com/VapourApps/va_master.git
    - target: /opt/va_master

npm-build:
  cmd.run:
    - name: npm install --no-bin-links && node build.js
    - cwd: /opt/va_master/va_dashboard