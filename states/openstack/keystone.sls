{% set fqdn = grains['host'] %}
keystone:
  pkg.installed

replace_connection:
  file.replace:
    - name: /etc/keystone/keystone.conf
    - pattern: connection = sqlite:////var/lib/keystone/keystone.db
    - repl: connection = mysql+pymysql://keystone:{{grains['keystone_dbpass']}}@localhost/keystone

uncomment_provider:
  file.uncomment:
    - name: /etc/keystone/keystone.conf
    - regex: provider = fernet

keystone-manage db_sync:
  cmd.run:
    - runas: keystone
    - shell: /bin/sh
    - cwd: ~

keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone:
  cmd.run

keystone-manage credential_setup --keystone-user keystone --keystone-group keystone:
  cmd.run

keystone-manage bootstrap --bootstrap-password {{grains['admin_pass']}} --bootstrap-admin-url http://{{fqdn}}:35357/v3/ --bootstrap-internal-url http://{{fqdn}}:35357/v3/ --bootstrap-public-url http://{{fqdn}}:5000/v3/ --bootstrap-region-id RegionOne:
  cmd.run

/root/keystonerc_admin:
  file.managed:
    - source: salt://openstack/files/keystonerc_admin
    - template: jinja
    - context:
      admin_pass: {{grains['admin_pass']}}
      admin_user: admin
      tenant: admin
      controller: {{fqdn}}

apache2:
  service.running:
    - watch:
      - file: /root/keystonerc_admin

source /root/keystonerc_admin && openstack project create --domain default --description "Service Project" service:
  cmd.run:
    - unless: source keystonerc_admin && openstack project list |grep -q service

source /root/keystonerc_admin && openstack role create user:
  cmd.run:
    - unless: source keystonerc_admin && openstack role list| grep -q user

source /root/keystonerc_admin && nopenstack role add --project admin --user admin user:
  cmd.run
