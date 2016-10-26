salt/dns:
  event.send:
    - data:                                                                                                                                                    
        name: {{ grains['id'] }}                                                                                                                               
        ip: {{ grains['ip4_interfaces']['eth0'][0] }}                                                                                                          
