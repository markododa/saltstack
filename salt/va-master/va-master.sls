salt://va-master/node-repo.sh:
  cmd.script:
    - onlyif: test ! -e /etc/apt/sources.list.d/nodesource.list

install_pkgs:
  pkg.installed:
    - pkgs:
      - wget
      - libvirt-dev
      - python-pip
      - build-essential
      - python-dev
      - libssl-dev
      - libffi-dev
      - libzmq3-dev
      - unzip
      - supervisor
      - curl
      - nodejs
      - salt-master
      - salt-cloud
      - git
      - rsyslog
      - libjpeg-dev
      - libvirt-clients
      - lxc-dev

python-libvirt:
  pkg.installed:
    - install_recommends: False

pip install --upgrade setuptools :
  cmd.run

va_master:
  git.latest:
    - name: https://github.com/VapourApps/va_master.git
    - target: /opt/va_master

cd /opt/va_master; git checkout {{salt['pillar.get']('va-master-branch','master')}}:
  cmd.run

/etc/systemd/system/va-master.service:
  file.managed:
    - source: salt://va-master/va-master.service
    
systemctl enable va-master --now:
 cmd.run:
      - unless: test -f  /.dockerenv

npm-build:
  cmd.run:
    - name: npm install && node build.js
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
    - user: root
    - group: adm
    - makedirs: True
    - require:
      - install_pkgs

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

/etc/logrotate.d/rsyslog:
  file.line:
    - content: /var/log/vapourapps/va-master.log
    - after: /var/log/syslog
    - mode: ensure

