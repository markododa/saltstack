import subprocess, json
import salt, sys
from monitoring_stats import parse


panel = {"monitoring.icinga":{"title":"Icinga proxy","content":[{"type":"Frame","name":"frame","src":"/proxy/"}]},"monitoring.chart":{"title":"","content":[{"type":"Chart","name":"chart","reducers": ["panel"]}]},"monitoring.status":{"title":"Status","tbl_source":{},"content":[{"type":"MultiTable","name":"div","reducers":["table"],"elements":[{"type":"Heading","dc":"monitoring :num: services"},{"type":"Table","reducers":["table","panel","alert"],"columns":[{"key":"name","label":"Name"},{"key":"output","label":"Output"},{"key":"state","label":"State"},{"key":"action","label":"Actions"}],"panels":{"view_graph":"monitoring.graph"},"rowStyleCol":"state","actions":[{"name":"View graphs","action":"chart"}],"id":"name"}]}]}}

def get_panel(panel_name, host='', service=''):
    users_panel = panel[panel_name]
    if panel_name == 'monitoring.chart':
        data = parse(host, service)
        users_panel['title'] = host + ' - ' + service
        users_panel['content'][0]['data'] = data
    else:
        data = icinga2()
        data = { x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data
    return users_panel


def icinga2():
    out = subprocess.check_output(['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out = json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts = {}
    service_state_names = {"0": "OK", "1": "Warning", "2": "Critical", "3": "Down"}
    for service_obj in json_out:
      host = service_obj['host_name']
      service = {'name': service_obj['service_description'],
                 'state': service_state_names[service_obj['service_state']],
                 'output': service_obj['service_output']}
      if host in hosts:
         hosts[host].append(service)
      else:
         hosts[host] = [service]

    # Now the data is structured, but it has no schema (each host is a key)
    # We want to transform [{'host1': data}, ...] into [{'name': host1, data}, ...]
    # So that we have an API friendly result

    formatted_hosts = []
    for host in hosts:
       formatted_hosts.append({'host_name': host, 'services': hosts[host]})

    return formatted_hosts
