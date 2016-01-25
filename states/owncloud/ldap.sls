setup:
  cmd.run:
    - name: |
        ./occ ldap:create-empty-config
        ./occ ldap:set-config '' ldapAgentName {{ salt['pillar.get']('agentname', '') }}
        ./occ ldap:set-config '' ldapAgentPassword {{ salt['pillar.get']('agentpass', '') }}
        ./occ ldap:set-config '' ldapBase {{ salt['pillar.get']('ldapbase', '') }}
        ./occ ldap:set-config '' ldapBaseGroups {{ salt['pillar.get']('ldapbasegroups', '') }}
        ./occ ldap:set-config '' ldapBaseUsers {{ salt['pillar.get']('ldapbaseusers', '') }}
        ./occ ldap:set-config '' ldapConfigurationActive '1'
        ./occ ldap:set-config '' ldapGroupFilter '(objectClass=group)'
        ./occ ldap:set-config '' ldapGroupFilterMode '1'
        ./occ ldap:set-config '' ldapGroupMemberAssocAttr 'member'
        ./occ ldap:set-config '' ldapHost {{ salt['pillar.get']('ldaphost', '') }}
        ./occ ldap:set-config '' ldapLoginFilter '(sAMAccountName=%uid)'
        ./occ ldap:set-config '' ldapLoginFilterMode '1'
        ./occ ldap:set-config '' ldapPort '389'
        ./occ ldap:set-config '' ldapUserDisplayName 'displayname'
        ./occ ldap:set-config '' ldapUserFilter '(objectClass=*)'
        ./occ ldap:set-config '' ldapUserFilterMode '1'
    - cwd: /var/www/owncloud/
    - user: www-data
    - group: www-data
