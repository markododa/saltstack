glance:
  pkg.installed

{% set fqdn = grains['host'] %}

source /root/keystonerc_admin && openstack user create --domain default --password {{grains['glance_pass']}} glance:
  cmd.run:
    - unless: source keystonerc_admin && openstack user list |grep -q glance

source /root/keystonerc_admin && openstack role add --project service --user glance admin:
  cmd.run

source /root/keystonerc_admin && openstack service create --name glance --description "OpenStack Image" image:
  cmd.run:
    - unless: source keystonerc_admin && openstack service list |grep -q glance

create_glance_endpoints:
  cmd.run:
    - name: |
        source /root/keystonerc_admin && openstack endpoint create --region RegionOne image public http://{{fqdn}}:9292
        source /root/keystonerc_admin && openstack endpoint create --region RegionOne image internal http://{{fqdn}}:9292
        source /root/keystonerc_admin && openstack endpoint create --region RegionOne image admin http://{{fqdn}}:9292
    - unless: source keystonerc_admin && openstack endpoint list |grep -q glance

{% for file in ['/etc/glance/glance-api.conf', '/etc/glance/glance-registry.conf'] %}
{{file}}_connection:
  file.replace:
    - name: {{file}}
    - pattern: "#connection = <None>"
    - repl: connection = mysql+pymysql://glance:{{grains['glance_dbpass']}}@localhost/glance

{{file}}_keystone_authtoken:
  file.blockreplace:
    - template: jinja
    - name: {{file}}
    - source: salt://openstack/files/keystone_authtoken
    - marker_start: |
        [keystone_authtoken]
    - marker_end: '#'
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['glance_pass']}}
        service: glance
{% endfor %}

{% for line in ['flavor = keystone', 'stores = file,http', 'default_store = file', 'filesystem_store_datadir = /var/lib/glance/images'] %}
{{line}}:
  file.uncomment:
    - name: /etc/glance/glance-api.conf
    - regex: {{line}}
{% endfor %}

glance-manage db_sync:
  cmd.run:
    - runas: glance
    - shell: /bin/sh
    - cwd: ~

glance-registry:
  service.running:
    - restart: True

glance-api:
  service.running:
    - restart: True

