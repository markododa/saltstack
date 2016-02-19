base:
  'role:monitoring':
    - match: grain
    - credentials
    - openstack
  'role:directory':
    - match: grain
    - directory
  'role:storage':
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
    - fileshare
    - directory
  '*':
    - base
