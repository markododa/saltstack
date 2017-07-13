{% if pillar['dcip'] is defined %}
echo ok:
  - cmd.run
{% elif pillar['dcip'] is not defined % }
echo not:
  - cmd.run
