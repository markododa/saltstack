{% set data = data['data'] %}

add_host:
  local.state.single:
    - tgt: 'role:monitoring'
    - tgt_type: grain
    - args:
      - fun: file.managed
      - name: /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - source: salt://monitoring/files/va_host.conf
      - template: jinja
      - context:
          INSTANCE_NAME: {{ data['name'] }}
          INSTANCE_IP: {{ data['ip'] }} 
          INSTANCE_TYPE: {{ data['type'] }} 

restart_icinga2:
  local.service.reload:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - icinga2
      - watch:
        - file: /etc/icinga2/conf.d/{{ data['name'] }}.conf
