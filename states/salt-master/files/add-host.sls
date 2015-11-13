add_host:
  local.file.copy:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /srv/salt/state/monitoring/files/va_host.conf
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf

instance_name:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern='{INSTANCE_NAME}'
      - repl='{{ data['name'] }}'

instance_ip:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern='{INSTANCE_IP}'
      - repl='{{ data['name']}}.novalocal'

instance_type:
  local.file.replace:
    - tgt: 'role:monitoring'
    - expr_form: grain
    - arg:
      - name: /etc/icinga2/conf.d/{{ data['name'] }}.conf
      - pattern: {INSTANCE_TYPE}
      - repl: {{ data['profile'] }}


#{% for x in data %}
#  {{ x }}:
#    local.file.append:
#      - tgt: 'role:monitoring'
#      - expr_form: grain
#      - arg:
#        - name: /root/output
#        - text: {{ x }}
#{% endfor %}
