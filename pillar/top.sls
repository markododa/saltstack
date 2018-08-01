base:
  'role:proxy':
    - match: grain
    - credentials
  'role:monitoring':
    - match: grain
    - credentials
    - openstack
  'role:directory':
    - match: grain
    - credentials
  'role:cloudshare':
    - match: grain
    - credentials
  'role:lamp':
    - match: grain
    - lamp
  'role:ticketing':
    - match: grain
    - credentials
    - ticketing
  'role:backup':
    - match: grain
    - credentials
  'role:fileshare':
    - match: grain
    - credentials
  'role:email':
    - match: grain
    - credentials
  'role:openvpn':
    - match: grain
    - openvpn
  'role:va-master':
    - match: grain
    - openvpn
    - credentials
    - ticketing
    - lamp
    - openstack
  'role:libvirt':
    - match: grain
    - credentials
  '*':
    - base
