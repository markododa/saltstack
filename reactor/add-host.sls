{% set data = data['data'] %}

add_host:
  local.file.copy:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /opt/va/icinga2/va-host.tmpl
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf

instance_name:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern="{INSTANCE_NAME}"
      - repl='{{ data['name'] }}'
      - backup=False

instance_ip:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern="^.*address = .*$"
      - repl=" address = '{{ data['ip']}}'"
      - backup=False

instance_type:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern="{INSTANCE_TYPE}"
      - repl={{ data['type'] }}
      - backup=False

restart_icinga2:
  local.service.reload:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - icinga2
      - watch:
        - file: /etc/icinga2/conf.d/{{ data['name'] }}.conf
