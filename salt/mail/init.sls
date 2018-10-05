{% if salt['pillar.get']('dcip') == '' %}
{% set dcip = salt['mine.get'](tgt='role:directory',fun='address',expr_form='grain')['va-directory'][0] %}
{% endif %}
{% if salt['pillar.get']('dcip') != '' %}
{% set dcip = salt['pillar.get']('dcip') %}
{% endif %}
{% set domain = salt['pillar.get']('domain') %}
{% set disk = salt['pillar.get']('disk', '/dev/vdb') %}
{% set query_user = salt['pillar.get']('query_user') %}
{% set ldap_field = salt['pillar.get']('ldap_field','userPrincipalName') %}
{% set query_password = salt['pillar.get']('query_password')  %}
{% set search_base = domain|replace(".", ",dc=") %}
{% set iredmail_version = '0.9.8' %}

postfix-ldap:
  pkg.installed: []

dovecot-ldap:
  pkg.installed: []

python-netaddr:
  pkg.installed: []

ldap-utils:
  pkg.installed: []


/root/:
  archive.extracted:
    - source: salt://mail/iRedMail-{{iredmail_version}}.tar.bz2
    - archive_format: tar
    - if_missing: /root/iRedMail-{{iredmail_version}}/

/root/iRedMail-{{iredmail_version}}/config:
  file.managed:
    - source: salt://mail/config
    - template: jinja
    - defaults:
        domain: {% filter lower %}{{ domain }}{% endfilter %}
        admin_password: {{ salt['pillar.get']('admin_password') }}
    - unless: test -f /root/iRedMail-{{iredmail_version}}/config

generate_passwords:
  cmd.run:
    - name: for x in $(seq $(grep random_password /root/iRedMail-{{iredmail_version}}/config |wc -l)); do sed -i "0,/random_password/s//`openssl rand -hex 10`/" /root/iRedMail-{{ iredmail_version }}/config; done
    - onlyif: grep -q random_password /root/iRedMail-{{iredmail_version}}/config 
install_iredmail:
  cmd.run:
    - name: bash iRedMail.sh
    - shell: /bin/bash
    - cwd: /root/iRedMail-{{iredmail_version}}/
    - env:
      - AUTO_USE_EXISTING_CONFIG_FILE: 'y'
      - AUTO_INSTALL_WITHOUT_CONFIRM: 'y'
      - AUTO_CLEANUP_REMOVE_SENDMAIL: 'y'
      - AUTO_CLEANUP_REMOVE_MOD_PYTHON: 'y'
      - AUTO_CLEANUP_REPLACE_FIREWALL_RULES: 'y'
      - AUTO_CLEANUP_RESTART_IPTABLES: 'y'
      - AUTO_CLEANUP_REPLACE_MYSQL_CONFIG: 'y'
      - AUTO_CLEANUP_RESTART_POSTFIX: 'n'
    - unless: test -e /var/vmail

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
        postmap hash:/etc/postfix/transport

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
        query_password: '{{ query_password }}'
        search_base: cn=users,dc={{ search_base }}
        result_attribute: {{ldap_field}}

/etc/dovecot/dovecot-ldap.conf:
  file.managed:
    - source: salt://mail/dovecot-ldap.conf
    - template: jinja
    - defaults:
        dcip: {{ dcip }}
        query_user: {{ query_user }}@{% filter lower %}{{ domain }}{% endfilter %}
        query_password: '{{ query_password }}'
        search_base: cn=users,dc={{ search_base }}
        ldap_field: {{ldap_field}}

dovecot_ldap_path:
  file.replace:
    - name: /etc/dovecot/dovecot.conf
    - pattern: /etc/dovecot/dovecot-pgsql.conf
    - repl: /etc/dovecot/dovecot-ldap.conf

dovecot_driver:
  file.replace:
    - name: /etc/dovecot/dovecot.conf
    - pattern: driver = sql
    - repl: driver = ldap

dovecot_quota:
  file.replace:
   - name: /etc/dovecot/dovecot.conf
   - pattern: "quota_rule = *:storage=1G"
   - repl: "quota_rule = *:storage=10G"

/etc/default/iptables:
  file.blockreplace:
    - marker_start: "#-A INPUT -p tcp --dport 5280 -j ACCEPT"
    - marker_end: "COMMIT"
    - content: "\n-A INPUT -p tcp --dport 5666 -j ACCEPT\n\n"

iptables:
  service.running:
    - watch:
      - file: /etc/default/iptables

{{ disk }}:
  blockdev.formatted:
    - onlyif:
        - test -e {{ disk }}

/mnt/va-email:
  mount.mounted:
    - device: {{ disk }}
    - fstype: ext4
    - mkmnt: True
    - onlyif:
        - test -e {{ disk }}
        
'mv /var/vmail /mnt/va-email/':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-email/
        - test ! -e /mnt/va-email/vmail
        - mount | grep -q /mnt/va-email

'ln -sfn /mnt/va-email/vmail /var/':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-email/vmail
        - mount | grep -q /mnt/va-email

#### functionality script
/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://mail/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

dovecot:
  service.running:
    - watch:
      - file: /etc/dovecot/*

postfix:
  service.running:
    - watch:
      - file: /etc/postfix/main.cf

/opt/va/:
  file.directory:
    - makedirs: True

/opt/va/panels.json:
  file.managed:
    - source: salt://mail/files/panels.json

{% set services = ['amavis-mc','amavis','amavisd-snmp-subagent','clamav-freshclam','fail2ban','nginx','php7.0-fpm'] %}
{% for service in services %}
{{ service }}:
  service.running:
    - watch:
      - file: /root/iRedMail-{{iredmail_version}}/config
{% endfor %}
