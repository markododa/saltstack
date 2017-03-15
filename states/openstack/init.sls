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

add-apt-repository cloud-archive:newton:
  cmd.run

apt update && apt -y dist-upgrade:
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

/etc/mysql/mariadb.conf.d/99-openstack.cnf:
  file.managed:
    - source: salt://openstack/files/99-openstack.cnf

mysql:
  service.running:
    - restart: True
    - watch:
      - file: /etc/mysql/mariadb.conf.d/99-openstack.cnf

rabbitmqctl add_user openstack {{grains['rabbit_pass']}}:
  cmd.run:
    - unless: rabbitmqctl  list_users| grep -q openstack

rabbitmqctl set_permissions openstack ".*" ".*" ".*":
  cmd.run

memcached:
  service.running:
    - restart: True
