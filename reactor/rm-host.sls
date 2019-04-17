remove:
  local.cmd.run:
    - tgt: 'role:monitoring'
    - tgt_type: grain
    - arg:
      - rm /etc/icinga2/conf.d/{{ data['name'] }}.conf

restart_icinga2:
  local.service.reload:
    - tgt: 'role:monitoring'
    - tgt_type: grain
    - arg:
      - icinga2 
