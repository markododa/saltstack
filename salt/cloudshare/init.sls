apt-transport-https:
  pkg.installed:
    - order: first
include:
  - cloudshare.mysql
  - cloudshare.repo
  - cloudshare.setup

{% if salt['pillar.get']('use_ldap',True) == True %}
include:
  - cloudshare.ldap
{% endif %}
