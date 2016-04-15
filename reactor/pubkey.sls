{% set data = data['data'] %}

copypubkey:
  local.file.write:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /srv/salt/backuppc/files/pubkey
      - '{{data['pubkey']}}'
