base:
  'role:monitoring':
    - match: grain
    - credentials
    - openstack
  'role:directory':
    - match: grain
    - credentials
    - openvpn
  'role:owncloud':
    - match: grain
    - owncloud
  'role:lamp':
    - match: grain
    - lamp
  'role:backup':
    - match: grain
    - credentials
  'role:fileshare':
    - match: grain
    - credentials
  '*':
    - base
