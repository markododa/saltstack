import subprocess, requests, json, re
from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_monitoring_panels import panels
from monitoring_stats import parse


def get_panel(panel_name, provider='', service=''):
    users_panel = panels[panel_name]
    if panel_name == 'monitoring.chart':
        if not provider or not service: 
            raise Exception('Provider and/or service not provided. Provider:%s service:%s' % (provider, service))
        data = parse(provider, service)
        users_panel['title'] = provider + ' - ' + service
        users_panel['content'][0]['data'] = data
        return users_panel
    elif panel_name == 'monitoring.status':
        data = icinga2()
        data = { x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data
        return users_panel

icinga_conf_template = 'object Host "%s" { \n\
  import "generic-host" \n\
  address = "%s" \n\
  display_name = "%s" \n\
  vars.notification["mail"] = { groups = [ "icingaadmins" ] } \n\
  vars.os="Windows" \n\
  vars.windesktop="False"'

def panel_overview():
    lines=[]
    output =  __salt__['cmd.run']('icingacli monitoring list --format "$host_name$ - $service_description$"')
    output= len(output.split('\n'))
    sender_dict = {
        'key' : 'Total services',
        'value' : output,
        }
    lines.append(sender_dict)

    output =  __salt__['cmd.run']('icingacli monitoring list')
    output= output.split('\n')
    thosts=0
    for x in output:
        if x=='': thosts=thosts+1
    sender_dict = {
        'key' : "Total hosts",
        'value' : thosts,
        }
    lines.append(sender_dict)

    output =  __salt__['cmd.run']('icinga2 feature list')
    output_lines = output.split('\n')
    #output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_separated = [[i for i in x.split(': ') if i] for x in output_lines]

    for x in output_lines_separated:
        if not x: continue
        if type(x) == str:
            lines[-1]['error'] = x
        elif len(x) > 1:
            sender_dict = {
                'key' : x[0],
                'value' : x[1].replace(' ',', '),
            }
            lines.append(sender_dict)

    try:
        f = __salt__['cmd.run']('cat /etc/ssmtp/ssmtp.conf')
    except: #TODO use specific Exception typ
        f = ''
    ssmtp_data = ssmtp_to_dict(f)

    sender_dict = {
        'key' : "Sending notifications from",
        'value' : ssmtp_data.get('AuthUser', ''),
        }
    lines.append(sender_dict)



    sender_dict = {
        'key' : "Mail server",
        'value' : ssmtp_data.get('mailhub', ''),
        }
    lines.append(sender_dict)


    sender_dict = {
        'key' : "Email password",
        'value': "Password is unconfigured/empty" if ssmtp_data.get('AuthPass', '')=='empty' else "Password is configured/non-empty",
    }
    lines.append(sender_dict)


    return lines


def ssmtp_to_dict(data):
     data = [x.strip() for x in data.split('\n') if x]

     data = [x for x in data if x[0] != '#' and '=' in x and x]
     data = dict([x.split('=') for x in data])
     return data


def add_host_to_icinga(host_name, ip_address, value_pairs = {}):
    conf_dir = '/etc/icinga2/conf.d/%s.conf' % host_name
    host_conf = icinga_conf_template % (host_name, ip_address, host_name)
    if value_pairs: 
        for pair in value_pairs: 
            host_conf += '\n  ' + pair + '="' + value_pairs[pair] + '"'
    host_conf += '\n}'

    with open(conf_dir, 'w') as f: 
        f.write(host_conf)

    try: 
        reload = subprocess.call(['service', 'icinga2', 'reload'])
    except:
        reload = True
    if reload: 
        subprocess.check_output(['service', 'icinga2', 'restart'])
    return True


def icinga2():
    out = subprocess.check_output(['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out = json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts = {}
    service_state_names = {"0": "OK", "1": "Warning", "2": "Critical", "3": "Unknown", '99': 'Pending'}
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
