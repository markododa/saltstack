base:
  '*':
    - nrpe.nrpe
  'role:va-monitoring':
    - match: grain
    - monitoring.icingaweb2
    - salt-master.salt
  'role:va-directory':
    - match: grain
    - directory.directory
  'role:va-storage':
    - match: grain
    - owncloud
