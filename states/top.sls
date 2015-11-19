base:
  '*':
    - nrpe.nrpe
  'role:monitoring':
    - match: grain
    - monitoring.icingaweb2
    - salt-master.salt
  'role:directory':
    - match: grain
    - directory.directory
  'role:owncloud':
    - match: grain
    - owncloud
