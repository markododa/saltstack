{% set adduser = 'openstack user create --domain default --password '+grains['nova_pass']+' nova' %}
{% set fqdn = grains['host'] %}

install-nova:
  pkg.installed:
    - pkgs:
      - nova-api
      - nova-conductor
      - nova-consoleauth
      - nova-novncproxy
      - nova-scheduler

{% for cmd in [ adduser, 'openstack role add --project service --user nova admin', 'openstack service create --name nova --description "OpenStack Compute" compute'] %}
source /root/keystonerc_admin && {{cmd}}:
  cmd.run:
    - unless: source /root/keystonerc_admin && openstack service list | grep -q nova
{% endfor %}

{% for endpoint in ['public', 'internal', 'admin'] %}
source keystonerc_admin && openstack endpoint create --region RegionOne compute {{endpoint}} http://{{fqdn}}:8774/v2.1/%\(tenant_id\)s:
  cmd.run:
    - unless: source keystonerc_admin && openstack endpoint list |grep -q 'nova.*{{endpoint}}'
{% endfor %}

nova_api_db_connection:
  file.blockreplace:
    - name: /etc/nova/nova.conf
    - marker_start: '[api_database]'
    - marker_end: '[oslo_concurrency]'
    - content: |
        connection = mysql+pymysql://nova:{{grains['nova_dbpass']}}@localhost/nova_api
         

nova_db_connection:
  file.blockreplace:
    - name: /etc/nova/nova.conf
    - marker_start: '[database]'
    - marker_end: '[api_database]'
    - content: |
        connection = mysql+pymysql://nova:{{grains['nova_dbpass']}}@localhost/nova
         

nova_rabbitmq_connection:
  file.blockreplace:
    - name: /etc/nova/nova.conf
    - marker_start: '[DEFAULT]'
    - marker_end: 'dhcpbridge_flagfile=/etc/nova/nova.conf'
    - content: |
        transport_url = rabbit://openstack:{{grains['rabbit_pass']}}@localhost
        auth_strategy = keystone
        my_ip = 127.0.0.1
        use_neutron = True
        firewall_driver = nova.virt.firewall.NoopFirewallDriver
        resume_guests_state_on_host_boot=True
        reclaim_instance_interval = 600


nova_keystone_authtoken:
  file.blockreplace:
    - template: jinja
    - name: /etc/nova/nova.conf
    - source: salt://openstack/files/keystone_authtoken
    - marker_start: '[keystone_authtoken]'
    - marker_end: '#End keystone authtoken block'
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['nova_pass']}}
        service: nova

lock_path:
  file.replace:
    - name: /etc/nova/nova.conf
    - pattern: /var/lock/nova
    - repl: /var/lib/nova/tmp

insert_nova_configs:
  file.blockreplace:
    - marker_start: '#Inserted nova config'
    - marker_end: '#End inserted nova config'
    - name: /etc/nova/nova.conf
    - source: salt://openstack/files/nova-append
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        my_ip: 127.0.0.1

nova-manage api_db sync:
  cmd.run:
    - runas: nova
    - shell: /bin/sh
    - cwd: ~

nova-manage db sync:
  cmd.run:
    - runas: nova
    - shell: /bin/sh
    - cwd: ~

{% for service in ['nova-api', 'nova-consoleauth', 'nova-scheduler', 'nova-conductor', 'nova-novncproxy'] %}
{{service}}:
  service.running:
    - watch:
      - file: /etc/nova/nova.conf
{% endfor %}
