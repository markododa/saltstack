base:
  'role:monitoring':
    - match: grain
    - icingaweb2
    - salt
  'role:directory':
    - match: grain
    - directory
  'role:storage':
    - match: grain
    - owncloud
  'role:backup':
    - match: grain
    - backuppc
  'role:lamp':
    - match: grain
    - lamp
  'role:fileshare':
    - match: grain
    - directory
  '*':
    - base
