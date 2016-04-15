{% import_yaml '/srv/pillar/credentials.sls' as credentials %}
mine_functions:
  inventory:
    - mine_function: grains.item
    - id
    - role
    - manufacturer
    - os
    - osarch
    - osmajorrelease
    - osrelease
    - num_cpus
    - cpu_model
    - cpuarch
    - mem_total
    - ip4_interfaces
    - virtual
    - fqdn
  address:
    mine_function: network.ip_addrs
    cidr: {{ credentials.subnet }}
