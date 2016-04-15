salt/backup/new:
  event.send:
    - data:
        name: {{ grains['id'] }} 
        ip: {{ grains['ip4_interfaces']['eth0'][0] }}
        type: {{ grains['role'] }}
        fqdn: {{ grains['fqdn'] }}
