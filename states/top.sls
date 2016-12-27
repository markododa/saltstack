base:
  '*':
    - base.nrpe
    - base.default
    - base.backup
  'role:monitoring':
    - match: grain
    - monitoring.icingaweb2
  'role:directory':
    - match: grain
    - directory.directory
  'role:fileshare':
    - match: grain
    - fileshare.fileshare
  'role:owncloud':
    - match: grain
    - owncloud
  'role:backup':
    - match: grain
    - backuppc
  'role:lamp':
    - match: grain
    - lamp.lamp
  'role:email':
    - match: grain
    - mail
  'role:proxy':
    - match: grain
    - proxy.proxy
  'role:va-master':
    - match: grain
    - va-master
    - openvpn
    - salt-master.salt
