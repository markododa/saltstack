{% set data = data['data'] %}

add_dns:
  local.va_directory.add_dns:
    - tgt: 'role:directory' 
    - tgt_type: grain
    - arg:
      - "{{ data['name'] }}"
      - "A"
      - {'address': {{ data['ip'] }} }
