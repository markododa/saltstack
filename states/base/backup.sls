{% set script = '' %}

{% if salt['cmd.retcode']("which mysqld") == 0 %}
{% set script = "/root/.va/db-backup.sh" %}

/root/.va/db-backup.sh:
  file.managed:
    - source: salt://base/files/db-backup.sh
    - mode: 755
    - makedirs: True

/root/.va/backup:
  file.directory:
    - order: last

{% endif %}

salt/backup/new:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{ grains['ip4_interfaces']['eth0'][0] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['fqdn'] }}
        script: {{ script }}
    - order: last
