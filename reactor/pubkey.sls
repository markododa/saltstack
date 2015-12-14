{% set data = data['data'] %}

remove:
  local.file.write:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /srv/salt/backuppc/files/pubkey
      - '{{data['pubkey']}}'
