{% set domain = salt['pillar.get']('domain') %}
{% set dcip = salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain')['va-directory']['ip4_interfaces']['eth0'][0] %}
{% set query_user = salt['pillar.get']('query_user') %}
{% set query_password = salt['pillar.get']('query_password')  %}
{% set search_base = domain|replace(".", ",dc=") %}

setup:
  cmd.run:
    - name: |
        ./occ app:enable 'user_ldap'
        ./occ ldap:delete-config ''
        ./occ ldap:create-empty-config
        ./occ ldap:set-config '' ldapAgentName '{{ salt['pillar.get']('query_user', '') }}@{{domain}}'
        ./occ ldap:set-config '' ldapAgentPassword '{{ salt['pillar.get']('query_password', '') }}'
        ./occ ldap:set-config '' ldapBase 'cn=Users,dc={{ search_base }}'
        ./occ ldap:set-config '' ldapBaseGroups 'cn=Groups,dc={{ search_base }}'
        ./occ ldap:set-config '' ldapBaseUsers 'cn=Users,dc={{ search_base }}'
        ./occ ldap:set-config '' ldapConfigurationActive '1'
        ./occ ldap:set-config '' ldapGroupFilter '(objectClass=group)'
        ./occ ldap:set-config '' ldapGroupFilterMode '1'
        ./occ ldap:set-config '' ldapGroupMemberAssocAttr 'member'
        ./occ ldap:set-config '' ldapHost {{ dcip }}
        ./occ ldap:set-config '' ldapLoginFilter '(sAMAccountName=%uid)'
        ./occ ldap:set-config '' ldapLoginFilterMode '1'
        ./occ ldap:set-config '' ldapPort '389'
        ./occ ldap:set-config '' ldapUserDisplayName 'displayname'
        ./occ ldap:set-config '' ldapUserFilter '(objectClass=*)'
        ./occ ldap:set-config '' ldapUserFilterMode '1'
        ./occ ldap:set-config '' ldapExpertUsernameAttr 'sAMAccountName'
    - cwd: /var/www/owncloud/
    - user: www-data
    - group: www-data
