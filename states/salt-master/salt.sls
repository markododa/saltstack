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
    - watch:
      - file: /etc/salt/master

restart_api:
  service.running:
    - name: salt-api
    - restart: True
    - watch:
      - service: salt-master

cloud-profiles:
    file.recurse:
        - name: /etc/salt/cloud.profiles.d/
        - source: salt://salt-master/files/cloud.profiles.d/

/etc/salt/master:
  file.managed:
    - source: salt://salt-master/files/master
    - template: jinja
    - context:
      openstackhost: {{ salt['pillar.get']('openstackhost')}}

configure_salt-cloud:
  file.managed:
    - name: /etc/salt/cloud.providers.d/vapps-openstack.conf
    - source: salt://salt-master/files/cloud.providers.d/vapps-openstack.conf
    - template: jinja
    - file_mode: 644
    - user: root
    - group: root
    - context:
      saltmaster: {{ salt['network.ip_addrs']('eth0').__getitem__(0) }}
      openstackhost: {{ salt['pillar.get']('openstackhost')}}
      openstackuser: {{ salt['pillar.get']('openstackuser')}}
      password: {{ salt['pillar.get']('openstackpass')}}
      tenant: {{ salt['pillar.get']('openstacktenant')}}
      ssh_key: {{ salt['pillar.get']('ssh_key')}}
      net_id: {{ salt['pillar.get']('net-id')}}

keystone-token-auth:
  file.managed:
    - name: /usr/lib/python2.7/dist-packages/salt/auth/keystone-token.py
    - source: salt://salt-master/files/keystone-token.py
    - file_mode: 644
    - user: root
    - group: root

/etc/hosts:
  file.append:
    
