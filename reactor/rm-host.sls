remove:
  local.cmd.run:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - rm /etc/icinga2/conf.d/{{ data['name'] }}.conf  
