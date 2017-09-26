salt/dns:
  event.send:
    - data:
        name: {{ grains['id'] }}
        ip: {{ salt['network.ipaddrs']()[0] }}
