{% set script = None %}

{% if salt['cmd.retcode']("which mysqld") == 0 or grains['host'] in ['va-owncloud','va-monitoring'] %}
{% set script = "/root/.va/db-backup.sh" %}

/root/.va/backup:
  file.directory:
    - makedirs: True

/root/.va/db-backup.sh:
  file.managed:
    - source: salt://base/files/db-backup.sh
    - mode: 755
    - makedirs: True

{% endif %}

salt/backup/new:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{salt['network.ip_addrs']()[-1] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['host'] }}.{% filter lower %}{{ salt['pillar.get']('domain') }}{% endfilter %}
        script: {{ script }}
    - order: last
