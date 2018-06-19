{% set data = data['data'] %}

{%set pubkey = salt['cmd.run']('cat /opt/backuppc-pubkey') %}
copy:
  local.ssh.set_auth_key_from_file:
    - tgt: {{ data['minion'] }}
    - expr_form: grain
    - arg:
      - root
      - /opt/backuppc-pubkey
