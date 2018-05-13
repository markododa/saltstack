{% set domain = salt['pillar.get']('domain') %}
{% if salt['pillar.get']('dcip') == '' %}
{% set dcip = salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain')['va-directory']['ip4_interfaces']['eth0'][0] %}
{% endif %}
{% if salt['pillar.get']('dcip') != '' %}
{% set dcip = salt['pillar.get']('dcip') %}
{% endif %}
{% set query_user = salt['pillar.get']('query_user') %}
{% set query_password = salt['pillar.get']('query_password')  %}
{% set search_base = domain|replace(".", ",dc=") %}
{% set ldap_conf = 'va-ldap' %}

setup:
  cmd.run:
    - runas: www-data
    - cwd: /var/www/owncloud/
    - name: |
        ./occ market:install user_ldap
        ./occ app:enable 'user_ldap'
        ./occ ldap:delete-config {{ ldap_conf }}
        ./occ ldap:create-empty-config {{ ldap_conf }}
        ./occ ldap:set-config {{ ldap_conf }} ldapAgentName '{{ salt['pillar.get']('query_user', '') }}@{{domain}}'
        ./occ ldap:set-config {{ ldap_conf }} ldapAgentPassword '{{ salt['pillar.get']('query_password', '') }}'
        ./occ ldap:set-config {{ ldap_conf }} ldapBase 'dc={{ search_base }}'
        ./occ ldap:set-config {{ ldap_conf }} ldapBaseGroups {{ ldap_conf }}
        ./occ ldap:set-config {{ ldap_conf }} ldapBaseUsers 'cn=Users,dc={{ search_base }}'
        ./occ ldap:set-config {{ ldap_conf }} ldapConfigurationActive '1'
        ./occ ldap:set-config {{ ldap_conf }} ldapGroupFilter '(objectClass=group)'
        ./occ ldap:set-config {{ ldap_conf }} ldapGroupFilterMode '1'
        ./occ ldap:set-config {{ ldap_conf }} ldapGroupMemberAssocAttr 'member'
        ./occ ldap:set-config {{ ldap_conf }} ldapHost {{ dcip }}
        ./occ ldap:set-config {{ ldap_conf }} ldapLoginFilter '(sAMAccountName=%uid)'
        ./occ ldap:set-config {{ ldap_conf }} ldapLoginFilterMode '1'
        ./occ ldap:set-config {{ ldap_conf }} ldapPort '389'
        ./occ ldap:set-config {{ ldap_conf }} ldapUserDisplayName 'displayname'
        ./occ ldap:set-config {{ ldap_conf }} ldapUserFilter '(objectClass=*)'
        ./occ ldap:set-config {{ ldap_conf }} ldapUserFilterMode '1'
        ./occ ldap:set-config {{ ldap_conf }} ldapExpertUsernameAttr 'sAMAccountName'
