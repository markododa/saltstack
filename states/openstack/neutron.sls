{% set neutron_user_create = 'openstack user create --domain default --password '+grains['neutron_pass']+'  neutron' %}
{% set neutron_role_create = 'openstack role add --project service --user neutron admin' %}
{% set neutron_service_create = 'openstack service create --name neutron --description "OpenStack Networking" network' %}
{% set fqdn = grains['host'] %}

{% for cmd in [neutron_user_create, neutron_role_create, neutron_service_create] %}
source /root/keystonerc_admin && {{cmd}}:
  cmd.run:
    - unless: source keystonerc_admin && openstack service list| grep -q neutron
{% endfor %}

{% for endpoint in ['public', 'internal', 'admin'] %}
source keystonerc_admin && openstack endpoint create --region RegionOne network {{endpoint}} http://{{fqdn}}:9696:
  cmd.run:
    - unless: source keystonerc_admin && openstack endpoint list |grep -q 'neutron.*{{endpoint}}'
{% endfor %}

install_neutron:
  pkg.installed:
    - pkgs:
      - neutron-server
      - neutron-plugin-ml2
      - neutron-linuxbridge-agent
      - neutron-l3-agent
      - neutron-dhcp-agent
      - neutron-metadata-agent

replace_connection_neutron:
  file.replace:
    - name: /etc/neutron/neutron.conf
    - pattern: connection = sqlite:////var/lib/neutron/neutron.sqlite
    - repl: connection = mysql+pymysql://neutron:{{grains['neutron_dbpass']}}@localhost/neutron

service_plugins_add:
  file.replace:
    - name: /etc/neutron/neutron.conf
    - pattern: '#service_plugins ='
    - repl: service_plugins = router

allow_overlapping_ips:
  file.replace:
    - name: /etc/neutron/neutron.conf
    - pattern: '#allow_overlapping_ips.*'
    - repl: allow_overlapping_ips = True

neutron_rabbitmq_connection:
  file.blockreplace:
    - name: /etc/neutron/neutron.conf
    - marker_start: |
        [DEFAULT]
    - marker_end: '#'
    - content: |
        transport_url = rabbit://openstack:{{grains['rabbit_pass']}}@localhost

neutron_auth_strategy:
  file.uncomment:
    - name: /etc/neutron/neutron.conf
    - regex: auth_strategy = keystone

neutron_keystone_authtoken:
  file.blockreplace:
    - template: jinja
    - name: /etc/neutron/neutron.conf
    - source: salt://openstack/files/keystone_authtoken
    - marker_start: |
        [keystone_authtoken]
    - marker_end: '#'
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['neutron_pass']}}
        service: neutron

notify_nova_uncomment:
  file.uncomment:
    - name: /etc/neutron/neutron.conf
    - regex: notify_nova_on_port


neutron_nova:
  file.blockreplace:
    - template: jinja
    - name: /etc/neutron/neutron.conf
    - source: salt://openstack/files/keystone_authtoken
    - marker_start: |
        [nova]
    - marker_end: '#'
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['nova_pass']}}
        service: nova

neutron_type_drivers:
  file.replace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - pattern: '#type_drivers = local,flat,vlan,gre,vxlan,geneve' 
    - repl: type_drivers = flat,vlan,vxlan

tenant_network_types:
  file.replace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - pattern: '#tenant_network_types = local'
    - repl: tenant_network_types = vxlan

mechanism_drivers:
  file.replace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - pattern: '#mechanism_drivers ='
    - repl: mechanism_drivers = linuxbridge,l2population

extension_drivers:
  file.replace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - pattern: '#extension_drivers ='
    - repl: extension_drivers = port_security

flat_networks:
  file.replace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - pattern: '#flat_networks = *$'
    - repl: flat_networks = provider

vni_ranges:
  file.blockreplace:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - marker_start: |
        [ml2_type_vxlan]
    - marker_end: '#'
    - content: vni_ranges = 1:1000


enable_ipset:
  file.uncomment:
    - name: /etc/neutron/plugins/ml2/ml2_conf.ini
    - regex: enable_ipset = true

physical_interface_mappings:
  file.replace:
    - name: /etc/neutron/plugins/ml2/linuxbridge_agent.ini
    - pattern: '#physical_interface_mappings ='
    - repl: physical_interface_mappings = provider:{{pillar['provider_interface']}}

vxlan:
  file.blockreplace:
    - name: /etc/neutron/plugins/ml2/linuxbridge_agent.ini
    - marker_start: |
        [vxlan]
    - marker_end: '#'
    - content: |
        enable_vxlan = True
        local_ip = 127.0.0.1
        l2_population = True

securitygroup:
  file.blockreplace:
    - name: /etc/neutron/plugins/ml2/linuxbridge_agent.ini
    - marker_start: |
        [securitygroup]
    - marker_end: '#'
    - content: |
        enable_security_group = True
        firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

l3_agent:
  file.replace:
    - name: /etc/neutron/l3_agent.ini
    - pattern: '#interface_driver = <None>'
    - repl: interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver

dhcp_agent:
  file.blockreplace:
    - name: /etc/neutron/dhcp_agent.ini
    - marker_start: |
        [DEFAULT]
    - marker_end: '#'
    - content: |
        interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver
        dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
        enable_isolated_metadata = True

nova_metadata_ip:
  file.uncomment:
    - name: /etc/neutron/metadata_agent.ini
    - regex: nova_metadata_ip = 127.0.0.1

metadata_proxy_shared_secret:
  file.replace:
    - name: /etc/neutron/metadata_agent.ini
    - pattern: '#metadata_proxy_shared_secret ='
    - repl: metadata_proxy_shared_secret = {{grains['metadata_proxy_shared_secret']}}

nova_neutron_settings:
  file.blockreplace:
    - template: jinja
    - name: /etc/nova/nova.conf
    - source: salt://openstack/files/nova_netron_section
    - marker_start: |
        [neutron]
    - marker_end: '#'
    - append_if_not_found: True
    - context:
        fqdn: {{grains['host']}}
        service_pass: {{grains['neutron_pass']}}
        service: neutron
        metadata_secret: {{grains['metadata_proxy_shared_secret']}}

neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head:
  cmd.run:
    - runas: neutron
    - shell: /bin/sh
    - cwd: ~

{% for service in ['nova-api', 'neutron-server', 'neutron-linuxbridge-agent', 'neutron-dhcp-agent', 'neutron-metadata-agent', 'neutron-l3-agent'] %}
{{service}}:
  service.running:
    - watch:
      - file: /etc/neutron/neutron.conf
{% endfor %}

