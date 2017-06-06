{% set data = data['data'] %}

copypubkey:
  local.file.write:
    - tgt: 'role:va-master'
    - expr_form: grain
    - arg:
      - /srv/salt/backuppc/files/pubkey
      - '{{data['pubkey']}}'
