import subprocess, json
import salt, sys


panel = {"status":{"title":"","tbl_source":{},"content":[{"type":"MultiTable","name":"div","reducers":["table"],"elements":[{"type":"Heading","dc":"monitoring :num: services"},{"type":"Table","reducers":["table","panel","alert"],"columns":[{"key":"name","label":"Name"},{"key":"state","label":"State"},{"key":"action","label":"Actions"}],"panels":{"view_graph":"monitoring.graph"},"actions":[{"name":"View graphs","action":"view_graph"}],"id":"name"}]}]}}

def get_panel(panel_name): 
    data = icinga2().local
    users_panel = panel[panel_name]
    data = { x['host_name']: x['services'] for x in data}
    users_panel['tbl_source'] = data
    return users_panel



def icinga2():
    out = subprocess.check_output(['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out = json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts = {}
    for service_obj in json_out:
      host = service_obj['host_name']
      service = {'name': service_obj['service_description'],
                 'state': int(service_obj['service_state']),
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
