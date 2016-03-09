base:
  '*':
    - base.nrpe
    - base.default
  'role:monitoring':
    - match: grain
    - monitoring.icingaweb2
    - salt-master.salt
  'role:directory':
    - match: grain
    - directory.directory
  'role:fileshare':
    - match: grain
    - fileshare.fileshare
  'role:storage':
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
