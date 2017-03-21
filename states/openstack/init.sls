{% from "openstack/pass.jinja" import passwords with context %}

{% for password in passwords %}
{{password}}:
  module.run:
    - name: grains.get_or_set_hash
    - password: {{password}}
    - chars: 'abcdefghijklmnopqrstuvwxyz0123456789'
    - length: 10
    - m_name: {{password}}
{% endfor %}


software-properties-common:
  pkg.installed

add-apt-repository cloud-archive:newton:
  cmd.run:
    - require:
      - pkg: software-properties-common

apt-get update -y && apt-get upgrade -y:
  cmd.run

install_pkgs:
  pkg.installed:
    - pkgs:
      - python-openstackclient
      - mariadb-server
      - python-pymysql
      - rabbitmq-server
      - memcached
      - python-memcache

rm /etc/mysql/mariadb.conf.d/50-server.cnf:
  cmd.run

/etc/mysql/mariadb.conf.d/99-openstack.cnf:
  file.managed:
    - source: salt://openstack/files/99-openstack.cnf

mysql:
  service.running:
    - restart: True
    - watch:
      - file: /etc/mysql/mariadb.conf.d/99-openstack.cnf

rabbitmqctl add_user openstack {{salt['grains.get']('rabbit_pass')}}:
  cmd.run:
    - unless: rabbitmqctl  list_users| grep -q openstack

rabbitmqctl set_permissions openstack ".*" ".*" ".*":
  cmd.run

memcached:
  service.running:
    - restart: True
