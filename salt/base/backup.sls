{% set script_pre = None %}

{% if salt['cmd.retcode']("which mysqld") == 0 or grains['role'] in ['ticketing', 'cloudshare','monitoring'] %}
{% set script_pre = "/root/.va/db-backup.sh" %}

/root/.va/backup/readme:
  file.append:
    - makedirs: True
    - text: Backup folder for database dumps

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
        minion: {{ grains['id'] }} 
        ip: {{ salt['network.get_route'](salt['network.default_route']()[0]['gateway'])['source'] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['host'] + '.' + grains['domain'] }}
        script_pre: {{ script_pre }}
    - order: last
