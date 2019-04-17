{% set data = data['data'] %}

copypubkey:
  local.file.write:
    - tgt: 'role:va-master'
    - tgt_type: grain
    - arg:
      - /opt/backuppc-pubkey
      - '{{data['pubkey']}}'
