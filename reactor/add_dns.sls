{% set data = data['data'] %}

add_dns:
  local.samba.add_dns:
    - tgt: 'role:directory' 
