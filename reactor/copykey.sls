{% set data = data['data'] %}

{%set pubkey = salt['cmd.run']('cat /opt/backuppc-pubkey') %}
copy:
  local.ssh.set_auth_key_from_file:
    - tgt: fqdn:{{ data['fqdn'] }}
    - expr_form: grain
    - arg:
      - root
      - /opt/backuppc-pubkey
