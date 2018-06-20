openstack-dashboard:
  pkg.installed

openstack_host:
  file.replace:
    - name: /etc/openstack-dashboard/local_settings.py
    - pattern: 'OPENSTACK_HOST =.*'
    - repl: OPENSTACK_HOST = '{{grains['host']}}'

session_engine:
  file.blockreplace:
    - name: /etc/openstack-dashboard/local_settings.py
    - marker_start: 'memcached set CACHES to something like'
    - marker_end: CACHES = {
    - content: |
        
        SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
        
keystone_api_version:
  file.replace:
    - name: /etc/openstack-dashboard/local_settings.py
    - pattern: OPENSTACK_KEYSTONE_URL = "http://%s:5000/v2.0"
    - repl: OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3"

enable_multidomain:
  file.replace:
    - name: /etc/openstack-dashboard/local_settings.py
    - pattern: OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False
    - repl: OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True

add_api_versions:
  file.blockreplace:
    - name: /etc/openstack-dashboard/local_settings.py
    - marker_start: |
        #Openstack API versions
    - marker_end: |
        #End openstack api versions block
    - append_if_not_found: True
    - content: |
        OPENSTACK_API_VERSIONS = {
            "identity": 3,
            "image": 2,
            "volume": 2,
        }

set_default_domain:
  file.uncomment:
    - name: /etc/openstack-dashboard/local_settings.py
    - regex: OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'default'

default_role:
  file.replace:
    - name: /etc/openstack-dashboard/local_settings.py
    - pattern: OPENSTACK_KEYSTONE_DEFAULT_ROLE = "_member_"
    - repl: OPENSTACK_KEYSTONE_DEFAULT_ROLE = "user"

restart_apache2:
  service.running:
    - name: apache2
    - watch:
      - file: /etc/openstack-dashboard/local_settings.py 
