{% set data = data['data'] %}

add_dns:
  local.samba.add_dns:
    - tgt: 'role:directory' 
    - expr_form: grain
    - arg:
      - "{{ data['name'] }}"
      - "A"
      - {'address': {{ data['ip'] }} }
