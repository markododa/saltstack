base:
  'role:monitoring':
    - match: grain
    - icingaweb2
    - salt
  'role:directory':
    - match: grain
    - directory
  'role:owncloud':
    - match: grain
    - owncloud
