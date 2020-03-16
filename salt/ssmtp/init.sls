{% set mail = salt['pillar.get']('ssmtp_mail') %}
{% set password = salt['pillar.get']('ssmtp_password') %}
{% set mxsrv = salt['pillar.get']('ssmtp_server') %}
{% set port = salt['pillar.get']('ssmtp_port') %}
{% set fqdn = grains['fqdn'] %}
{% set local_mail_user = salt['pillar.get']('local_mail_user', 'root')  %}

ssmtp:
  pkg.installed


/etc/ssmtp/ssmtp.conf:
  file.managed:
    - source: salt://ssmtp/ssmtp.conf
    - template: jinja
    - context:
        mail: {{mail}}
        password: {{password}}
        mxsrv: {{mxsrv}}
        port: {{port}}
        fqdn: {{fqdn}}

/etc/ssmtp/revaliases:
  file.append:
    - text: {{local_mail_user}}:{{mail}}
