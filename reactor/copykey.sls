{% set data = data['data'] %}

copy:
  local.ssh.set_auth_key_from_file:
    - tgt: fqdn:{{ data['fqdn'] }}
    - expr_form: grain
    - arg:
      - root
      - salt://backuppc/files/pubkey
