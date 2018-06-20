{% set data = data['data'] %}

{%set pubkey = salt['cmd.run']('cat /opt/backuppc-pubkey') %}
copy:
  local.ssh.set_auth_key:
    - tgt: {{data['minion']}}
    - arg:
      - root
      - {{pubkey}}
