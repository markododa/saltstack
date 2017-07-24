{% if pillar['dcip'] is defined %}
include:
  - directory.directory_join
{% elif pillar['dcip'] is not defined %}
include:
  - directory.directory
{% endif %}
