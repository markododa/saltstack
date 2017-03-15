{% set cinder_user_create = 'openstack user create --domain default --password '+grains['cinder_pass']+'  cinder' %}
{% set cinder_role_create = 'openstack role add --project service --user cinder admin' %}
{% set cinder_service_create = 'openstack service create --name cinder --description "OpenStack Block Storage" volume' %}
{% set cinderv2_service_create = 'openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2' %}
{% set fqdn = grains['host'] %}

{% for cmd in [cinder_user_create, cinder_role_create, cinder_service_create, cinderv2_service_create] %}
source /root/keystonerc_admin && {{cmd}}:
  cmd.run:
    - unless: source keystonerc_admin && openstack service list| grep -q volumev2
{% endfor %}

{% set volume = 'volume' %}
{% for endpoint_url in ['http://'+grains['host']+':8776/v1/%\(tenant_id\)s', 'http://'+grains['host']+':8776/v2/%\(tenant_id\)s'] %}
{% for endpoint in ['public', 'internal', 'admin'] %}
{%if endpoint_url == 'http://'+grains['host']+':8776/v2/%\(tenant_id\)s' %}
{% set volume = 'volumev2' %}
{% endif %}
source keystonerc_admin && openstack endpoint create --region RegionOne {{volume}} {{endpoint}} {{endpoint_url}}:
  cmd.run:
    - unless: source keystonerc_admin && openstack endpoint list |grep -q '{{volume}}.*{{endpoint}}'
{% endfor %}
{% endfor %}

install_cinder_api:
  pkg.installed:
    - pkgs:
      - cinder-api
      - cinder-scheduler

replace_connection_cinder:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[database]'
    - content: |
        connection = mysql+pymysql://cinder:{{grains['cinder_dbpass']}}@localhost/cinder
    - marker_end: '#end database config'
    - append_if_not_found: True

add_transport_url:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[DEFAULT]'
    - marker_end: 'rootwrap_config = /etc/cinder/rootwrap.conf'
    - content: |
        transport_url = rabbit://openstack:{{grains['rabbit_pass']}}@localhost
        my_ip = 127.0.0.1

cinder_keystone_authtoken:
  file.blockreplace:
    - template: jinja
    - name: /etc/cinder/cinder.conf
    - source: salt://openstack/files/keystone_authtoken
    - marker_start: |
        [keystone_authtoken]
    - marker_end: '#End authtoken block'
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['cinder_pass']}}
        service: cinder

oslo_concurrency_cinder:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[oslo_concurrency]'
    - marker_end: '#End oslo_concurrency block'
    - append_if_not_found: True
    - content: |
        lock_path = /var/lib/cinder/tmp

cinder-manage db sync:
  cmd.run:
    - runas: cinder
    - shell: /bin/sh
    - cwd: ~

nova_cinder_config:
  file.blockreplace:
    - name: /etc/nova/nova.conf
    - marker_start: '[cinder]'
    - marker_end: '#End cinder block'
    - append_if_not_found: True
    - content: |
        os_region_name = RegionOne

{% for service in ['nova-api','cinder-scheduler','cinder-api'] %}
{{service}}:
  service.running:
    - watch:
      - file: /etc/cinder/cinder.conf
{% endfor %}
