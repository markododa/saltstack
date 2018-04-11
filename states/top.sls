base:
  '*':
    - base.default
    - base.backup
    - base.nrpe
    - base.dns
  'role:monitoring':
    - match: grain
    - monitoring.icingaweb2
  'role:directory':
    - match: grain
    - directory
  'role:fileshare':
    - match: grain
    - fileshare.fileshare
  'role:cloudshare':
    - match: grain
    - cloudshare
  'role:backup':
    - match: grain
    - backuppc
  'role:lamp':
    - match: grain
    - lamp.lamp
  'role:email':
    - match: grain
    - mail
  'role:ticketing':
    - match: grain
    - ticketing.ticketing
  'role:proxy':
    - match: grain
    - proxy.proxy
  'role:objectstore':
    - match: grain
    - objectstore.objectstore
  'role:va-master':
    - match: grain
    - va-master
    - openvpn
    - salt-master.salt
  'role:libvirt':
    - match: grain
    - libvirt
