{% set data = data['data'] %}
existing-to-new-app:
  local.state.sls:
    - tgt: '*'
    - arg:
      - {{data['sls']}}
