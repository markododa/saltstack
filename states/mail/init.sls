{% set domain = salt['pillar.get']('domain') %}
{% set dcip = salt['pillar.get']('dcip') %}
{% set query_user = salt['pillar.get']('query_user') %}
{% set query_password = salt['pillar.get']('query_password')  %}
{% set search_base = domain|replace(".", ",dc=") %}

postfix-ldap:
  pkg.installed: []

dovecot-ldap:
  pkg.installed: []

/etc/hostname:
  file.managed:
    - contents: mx


/etc/hosts:
  file.replace:
    - pattern: 127.0.0.1.*$
    - repl: 127.0.0.1 mx.{% filter lower %}{{ domain }}{% endfilter %} mx localhost

/root/:
  archive.extracted:
    - source: salt://mail/iRedMail-0.9.4.tar.bz2
    - archive_format: tar
    - if_missing: /root/iRedMail-0.9.4/

/root/iRedMail-0.9.4/config:
  file.managed:
    - source: salt://mail/config
    - template: jinja
    - defaults:
        domain: {% filter lower %}{{ domain }}{% endfilter %}
        admin_password: {{ salt['pillar.get']('admin_password') }}

generate_passwords:
  cmd.run:
    - name: for x in $(seq $(grep random_password /root/iRedMail-0.9.4/config |wc -l)); do sed -i "0,/random_password/s//`openssl rand -hex 10`/" /root/iRedMail-0.9.4/config; done

install_iredmail:
  cmd.run:
    - name: bash iRedMail.sh
    - shell: /bin/bash
    - cwd: /root/iRedMail-0.9.4/
    - env:
      - AUTO_USE_EXISTING_CONFIG_FILE: 'y'
      - AUTO_INSTALL_WITHOUT_CONFIRM: 'y'
      - AUTO_CLEANUP_REMOVE_SENDMAIL: 'y'
      - AUTO_CLEANUP_REMOVE_MOD_PYTHON: 'y'
      - AUTO_CLEANUP_REPLACE_FIREWALL_RULES: 'y'
      - AUTO_CLEANUP_RESTART_IPTABLES: 'y'
      - AUTO_CLEANUP_REPLACE_MYSQL_CONFIG: 'y'
      - AUTO_CLEANUP_RESTART_POSTFIX: 'n'

postconf:
  cmd.run:
    - name: |
        postconf -e virtual_alias_maps=''
        postconf -e sender_bcc_maps=''
        postconf -e recipient_bcc_maps=''
        postconf -e relay_domains=''
        postconf -e relay_recipient_maps=''
        postconf -e smtpd_sasl_local_domain='{{ domain }}'
        postconf -e virtual_mailbox_domains='{{ domain }}'
        postconf -e transport_maps='hash:/etc/postfix/transport'
        postconf -e smtpd_sender_login_maps='proxy:ldap:/etc/postfix/ad_sender_login_maps.cf'
        postconf -e virtual_mailbox_maps='proxy:ldap:/etc/postfix/ad_virtual_mailbox_maps.cf'
        postconf -e virtual_alias_maps='proxy:ldap:/etc/postfix/ad_virtual_group_maps.cf'

/etc/postfix/transport:
  file.managed:
    - contents: {{ domain }} dovecot

/etc/postfix/main.cf:
  file.comment:
    - regex: .*check_policy_service inet:127.0.0.1:7777

/etc/postfix/:
  file.recurse:
    - source: salt://mail/postfix
    - template: jinja
    - defaults:
        dcip: {{ dcip }}
        query_user: {{ query_user }}@{% filter lower %}{{ domain }}{% endfilter %}
        query_password: {{ query_password }}
        search_base: cn=users,dc={{ search_base }}

/etc/dovecot/dovecot-ldap.conf:
  file.managed:
    - source: salt://mail/dovecot-ldap.conf
    - template: jinja
    - defaults:
        dcip: {{ dcip }}
        query_user: {{ query_user }}@{% filter lower %}{{ domain }}{% endfilter %}
        query_password: {{ query_password }}
        search_base: cn=users,dc={{ search_base }}
