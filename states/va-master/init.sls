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
      - libzmq3-dev
      - unzip
      - supervisor
      - curl
      - python-libvirt
      - nodejs
      - python-setuptools
      - salt-master
      - salt-cloud
      - git
      - rsyslog

easy_install pip:
  cmd.run

wget -q https://releases.hashicorp.com/consul/0.7.4/consul_0.7.4_linux_amd64.zip:
  cmd.run:
    - creates: /root/consul_0.7.4_linux_amd64.zip

/usr/bin:
  archive.extracted:
    - source: /root/consul_0.7.4_linux_amd64.zip
    - enforce_toplevel: False

/etc/consul.d:
  file.directory

/etc/consul.d/consul.json:
  file.managed:
    - source: salt://va-master/consul.json

/etc/systemd/system/consul.service:
  file.managed:
    - source: salt://va-master/consul.service

consul:
  service.running:
    - enable: True
    - watch:
      - file: /etc/systemd/system/consul.service


va_master:
  git.latest:
    - name: https://github.com/VapourApps/va_master.git
    - target: /opt/va_master

/etc/systemd/system/va-master.service:
  file.managed:
    - source: salt://va-master/va-master.service

npm-build:
  cmd.run:
    - name: npm install --no-bin-links && node build.js
    - cwd: /opt/va_master/va_dashboard

pip_install:
  cmd.run:
    - name: pip install .
    - cwd: /opt/va_master

/etc/rsyslog.d/70-va-master.conf:
  file.managed:
    - source: salt://va-master/files/rsyslog-va-master.conf

rsyslog:
  service.running:
    - restart: True
    - watch:
      - file: /etc/rsyslog.d/70-va-master.conf

/var/log/vapourapps/va-master.log:
  file.managed:
    - user: syslog
    - group: adm
    - makedirs: True 

#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True

check_functionality_va_master:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://va-master/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755
