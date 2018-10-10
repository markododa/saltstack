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
  'role:backup4':
    - match: grain
    - backup4
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
  'role:wordpress':
    - match: grain
    - wordpress
  'role:objectstore':
    - match: grain
    - objectstore
  'role:va-master':
    - match: grain
    - va-master
    - openvpn
    - salt-master.salt
  'role:libvirt':
    - match: grain
    - libvirt
  'role:nginx':
    - match: grain
    - nginx
  'role:lxd':
    - match: grain
    - lxd
  'role:elk':
    - match: grain
    - elk
