salt/dns:
  event.send:
    - data:                                                                                                                                                    
        name: {{ grains['fqdn'] }}                                                                                                                               
        ip: {{ salt['network.ipaddrs']() }}                                                                                                          
