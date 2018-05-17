{% set data = data['data'] %}

copypubkey:
  local.file.write:
    - tgt: 'role:va-master'
    - expr_form: grain
    - arg:
      - /opt/backuppc-pubkey
      - '{{data['pubkey']}}'
