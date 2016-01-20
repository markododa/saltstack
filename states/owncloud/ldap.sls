{% from "owncloud/ldap.jinja" import commands with context %}
#{% for command in ["ldap:set-config '' ldapAgentName "+salt['pillar.get']('agentname', ''),"ldap:set-config '' ldapBase"+salt['pillar.get']('ldapbase', ''), ] %}
{% for command in commands %}
{{ command }}:
  cmd.run:
    - name: ./occ {{ command }}
    - cwd: /var/www/owncloud/
    - user: www-data
    - group: www-data
{% endfor %}
