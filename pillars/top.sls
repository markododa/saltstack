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
    - credentials
  'role:lamp':
    - match: grain
    - lamp
  'role:backup':
    - match: grain
    - credentials
  'role:fileshare':
    - match: grain
    - credentials
  'role:email':
    - match: grain
    - credentials
  '*':
    - base
