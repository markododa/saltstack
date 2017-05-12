lvm2:
  pkg.installed

{{pillar['cinder_pv']}}:
  lvm.pv_present

cinder-volumes:
  lvm.vg_present:
    - devices: {{pillar['cinder_pv']}}

cinder-volume:
  pkg.installed

replace_connection_cinder-node:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[database]'
    - content: |
        connection = mysql+pymysql://cinder:{{grains['cinder_dbpass']}}@localhost/cinder
    - marker_end: '#end database config'
    - append_if_not_found: True

add_transport_url_node:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[DEFAULT]'
    - marker_end: 'rootwrap_config = /etc/cinder/rootwrap.conf'
    - content: |
        transport_url = rabbit://openstack:{{grains['rabbit_pass']}}@localhost
        my_ip = 127.0.0.1
        enabled_backends = lvm
        glance_api_servers = http://{{grains['host']}}:9292


cinder_node_keystone_authtoken:
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

cinder_lvm_block:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - source: salt://openstack/files/cinder_lvm
    - marker_start: |
        [lvm]
    - marker_end: '#End lvm block'
    - append_if_not_found: True

oslo_concurrency_cinder-node:
  file.blockreplace:
    - name: /etc/cinder/cinder.conf
    - marker_start: '[oslo_concurrency]'
    - marker_end: '#End oslo_concurrency block'
    - append_if_not_found: True
    - content: |
        lock_path = /var/lib/cinder/tmp

tgt:
  service.running:
    - watch:
      - file: /etc/cinder/cinder.conf


cinder-volume-restart:
  service.running:
    - name: cinder-volume
    - watch:
      - file: /etc/cinder/cinder.conf
