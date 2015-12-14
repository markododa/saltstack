install_salt-pkgs:
  pkg.installed:
    - pkgs:
      - salt-master
      - salt-api
      - salt-cloud
      - python-libcloud
      - python-novaclient
      - python-glanceclient

restart_salt:
  service.running:
    - name: salt-master
    - restart: True

restart_api:
  service.running:
    - name: salt-api
    - restart: True

cloud-profiles:
    file.recurse:
        - name: /etc/salt/cloud.profiles.d/
        - source: salt://salt-master/files/cloud.profiles.d/

configure_salt-cloud:
  file.managed:
    - name: /etc/salt/cloud.providers.d/openstack.conf
    - source: salt://salt-master/files/cloud.providers.d/openstack.conf
    - file_mode: 644
    - user: root
    - group: root


/etc/salt/cloud.providers.d/openstack.conf:
  file.replace:
    - pattern: SALTMASTER
    - repl: {{ salt['network.ip_addrs']('eth0').__getitem__(0) }}

openstack_host:
  file.replace:
    - name: /etc/salt/cloud.providers.d/openstack.conf
    - pattern: OPENSTACKHOST
    - repl: {{ salt['pillar.get']('openstackhost')}}

openstack_user:
  file.replace:
    - name: /etc/salt/cloud.providers.d/openstack.conf
    - pattern: OPENSTACKUSER
    - repl: {{ salt['pillar.get']('openstackuser')}}

openstack_pass:
  file.replace:
    - name: /etc/salt/cloud.providers.d/openstack.conf
    - pattern: OPENSTACKPASS
    - repl: {{ salt['pillar.get']('openstackpass')}}

openstack_tenant:
  file.replace:
    - name: /etc/salt/cloud.providers.d/openstack.conf
    - pattern: OPENSTACKTENANT
    - repl: {{ salt['pillar.get']('openstacktenant')}}

keystone-token-auth:
  file.managed:
    - name: /usr/lib/python2.7/dist-packages/salt/auth/keystone-token.py
    - source: salt://salt-master/files/keystone-token.py
    - file_mode: 644
    - user: root
    - group: root
