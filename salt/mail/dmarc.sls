install_packages:
  pkg.installed:
    - names:
      - opendkim
      - opendmarc

opendmarc:
  service.running:
    - enable: True

opendkim:
  service.running:
    - enable: True

/etc/opendmarc.conf:
  file.append:
    - text:
      - AuthservID OpenDMARC
      - TrustedAuthservIDs {{ grains["fqdn"] }}
      - RejectFailures true
      - IgnoreAuthenticatedClients true
      - RequiredHeaders    true
      - SPFSelfValidate true
    - require:
       - pkg: install_packages
    - watch_in:
       - service: opendmarc

/var/spool/postfix/opendmarc:
  file.directory:
    - user: opendmarc
    - group: opendmarc
    - mode: 750

opendmarc_group:
  group.present:
    - name: opendmarc
    - members:
      - postfix

change_socket_opendmarc:
  file.replace:
    - name: /etc/opendmarc.conf
    - pattern: Socket local:/var/run/opendmarc/opendmarc.sock
    - repl: Socket local:/var/spool/postfix/opendmarc/opendmarc.sock
    - watch_in:
      - service: opendmarc
    - require:
      - group: opendmarc
      - file: /var/spool/postfix/opendmarc

/etc/opendkim.conf:
  file.append:
    - text: |
        Mode         v
        #OpenDKIM user
        # Remember to add user postfix to group opendkim
        UserID             opendkim
        # Hosts to ignore when verifying signatures
        ExternalIgnoreList  /etc/opendkim/trusted.hosts
        InternalHosts       /etc/opendkim/trusted.hosts
        Socket              local:/var/spool/postfix/opendkim/opendkim.sock
        require:
        - pkg: install_packages
    - watch_in:
      - service: opendkim

opendkim_group:
  group.present:
    - name: opendkim
    - members:
      - postfix

/var/spool/postfix/opendkim:
  file.directory:
    - user: opendkim
    - group: opendkim
    - mode: 750

/etc/opendkim/trusted.hosts:
  file.managed:
    - makedirs: True
    - contents: |
        127.0.0.1
        localhost
        *.{{grains['domain']}}
    - require:
        - pkg: install_packages

change_socket_opendkim:
  file.replace:
    - name: /etc/opendkim.conf
    - pattern: Socket local:/var/run/opendkim/opendkim.sock
    - repl: Socket local:/var/spool/postfix/opendkim/opendkim.sock
    - watch_in:
      - service: opendkim
    - require:
      - group: opendkim
      - file: /var/spool/postfix/opendkim

/etc/postfix/main.cf:
  file.append:
    - text: |
        # Milter configuration
        milter_default_action = accept
        milter_protocol = 6
        smtpd_milters = local:opendkim/opendkim.sock,local:opendmarc/opendmarc.sock
        non_smtpd_milters = $smtpd_milters

postfix:
  service.running:
    - watch:
      - file: /etc/postfix/main.cf
