base:
  'role:va-monitoring':
    - match: grain
    - icingaweb2
    - salt
  'role:va-directory':
    - match: grain
    - directory
  'role:va-storage':
    - match: grain
    - owncloud
  'role:va-backup':
    - match: grain
    - backuppc
