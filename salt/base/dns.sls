salt/dns:
  event.send:
    - data:
        name: {{ grains['id'] }}
        ip: {{ salt['network.get_route'](salt['network.default_route']()[0]['gateway'])['source'] }}
