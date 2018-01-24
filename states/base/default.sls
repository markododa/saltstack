timedatectl set-timezone {{ pillar['timezone'] }}:
  cmd.run:
    - require:
      - pkg: install_packages


install_packages:
  pkg.installed:
    - pkgs:
      - rsync
      - sudo
      - dbus

/root/.bashrc:
  file.append:
    - text:
      - export PS1='\[\033[1;33m\]\u\[\033[1;37m\]@\[\033[1;32m\]\h\[\033[1;37m\]:\[\033[1;31m\]\w \[\033[1;36m\]\$ \[\033[0m\]'
      - alias ls='ls --color=auto'
      - alias grep='grep --color=auto'
      - alias rm='rm -i'
      - alias cp='cp -i'
      - alias mv='mv -i'
      - export HISTTIMEFORMAT="%d/%m/%y %T "

{% if salt['grains.get']('role')  == None %}
{% set role='Application' %}
{% else %}
{% set role=salt['grains.get']('role') %}
{% endif %}

/etc/motd:
  file.managed:
    - source: salt://base/files/motd

hostname:
  file.replace:
    - name: /etc/motd
    - pattern: HOSTNAME
    - repl: {{ salt['grains.get']('fqdn') }}

description:
  file.replace:
    - name: /etc/motd
    - pattern: DESCRIPTION
    - repl: Vapour-Apps {{role}} server

os_release:
  file.replace:
    - name: /etc/motd
    - pattern: OS_RELEASE
    - repl: {{ salt['grains.get']('lsb_distrib_description') }}

contact:
  file.replace:
    - name: /etc/motd
    - pattern: CONTACT
    - repl: 'contact: support@vapour-apps.com'

fqdn:
  host.only:
    - name: 127.0.1.1
    - hostnames:
      - {{ grains['host'] }}.{% filter lower %}{{ salt['pillar.get']('domain') }}{% endfilter %}
      - {{ grains['host'] }}

saltutil.sync_grains:
  module.run

/etc/salt/minion:
  file.line:
    - content: "startup_states: highstate"
    - mode: delete
    - order: last


/etc/cloud/cloud.cfg:
  file.line:
    - content: 'manage_etc_hosts: true'
    - mode: delete
    - order: last
    - onlyif: test -e /etc/cloud/cloud.cfg
