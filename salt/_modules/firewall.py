import salt


def nat_rules():
    return __salt__['iptables.get_rules']()['nat']['PREROUTING']['rules']

def grep_nat(port):
    for item in nat_rules():
        if item['destination_port'] == [str(port)]:
            return item

def insert_nat(destination, destination_port, port):
    destination=str(destination)
    port=str(port)
    rule='-i eth0 -p tcp -d 10.107.150.20 --dport '+port+' -j DNAT --to-destination '+destination+':'+destination_port
    return __salt__['iptables.insert']('nat', 'PREROUTING', position=1, rule=rule)

def delete_nat(destination, port):
    destination=str(destination)
    port=str(port)
    rule='-i eth0 -p tcp -d 10.107.150.20 --dport '+port+' -j DNAT --to-destination '+destination+':'+destination_port
    return __salt__['iptables.delete']('nat', 'PREROUTING', rule=rule)
