import subprocess
import requests
import json
import re
import time, datetime
import salt
from requests.auth import HTTPBasicAuth

from va_utils import check_functionality as panel_check_functionality
from va_utils import restart_functionality as restart_functionality
from va_monitoring_panels import panels
from monitoring_stats import parse
from monitoring_stats import parse_multichart

#Using this to convert from integer states to icinga states( 0 = OK, 1 = WARNING etc. )
states = {0 : 'OK', 1 : 'Warning', 2 : 'Critical', 3 : 'Unknown', 99 : 'Pending'} #NINO
states = ['OK', 'Warning', 'Critical', 'Unknown']

user = 'admin'

def get_password():
    password = __salt__['pillar.get']('admin_password') 
    return password

def get_ip():
    ip = __salt__['grains.get']('ipv4')
    ip = [x for x in ip if '127.0.0.1' not in x][0]
    return ip

def get_panel(panel_name, provider='', service=''):
    users_panel = panels[panel_name]
    if panel_name == 'monitoring.chart':
        if not provider or not service:
            raise Exception(
                'Provider and/or service not provided. Provider:%s service:%s' % (provider, service))
        data = parse(provider, service)
        users_panel['title'] = provider + ' - ' + service
        users_panel['content'][0]['data'] = data
        return users_panel
    elif panel_name == 'monitoring.multi_charts':
        data = parse_multichart(provider, service)
        users_panel['tbl_source'] = {x['host_name']: x['zharts'] for x in data}
        return users_panel
    elif panel_name == 'monitoring.multi_charts_1h':
        data = parse_multichart(provider, service)
        users_panel['tbl_source'] = {x['host_name']: x['zharts'] for x in data}
        return users_panel
    elif panel_name == 'monitoring.multi_charts_1d':
        data = parse_multichart(provider, service,'-1d','7200')
        # data = parse_multichart(provider, service,'-1d','1800')
        users_panel['tbl_source'] = {x['host_name']: x['zharts'] for x in data}
        return users_panel
    elif panel_name == 'monitoring.multi_charts_1w':
        data = parse_multichart(provider, service,'-7d','14400')
        users_panel['tbl_source'] = {x['host_name']: x['zharts'] for x in data}
        return users_panel
    elif panel_name == 'monitoring.problems':
        data = icinga2_problems()
        for host in data: 
            for service in host['services']:
                service['host_name'] = host['host_name'] 
        data1 = {x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data1
        return users_panel
    elif panel_name == 'monitoring.details':
        data = icinga2_singlehost(provider)
        for host in data: 
            for service in host['services']:
                service['host_name'] = host['host_name'] 
        data1 = {x['host_name']: x['services'] for x in data}
        users_panel['tbl_source'] = data1
        return users_panel
    elif panel_name == 'monitoring.history':
        data = icinga2()
        data1 = {x['host_name']: panel_history_events(x['host_name'],'*','1month') for x in data}
        users_panel['tbl_source'] = data1
        return users_panel


icinga_conf_template = 'object Host "%s" { \n\
    import "generic-host" \n\
    address = "%s" \n\
    vars.notification["mail"] = { groups = [ "icingaadmins" ] } \n\
    '


def panel_overview():
    lines = []
    output = __salt__['cmd.run'](
        'icingacli monitoring list --format "$host_name$ - $service_description$"')
    output = len(output.split('\n'))
    sender_dict = {
        'key': 'Total services',
        'value': output,
    }
    lines.append(sender_dict)

    output = __salt__['cmd.run']('icingacli monitoring list')
    output = output.split('\n')
    thosts = 0
    for x in output:
        if x == '':
            thosts = thosts+1
    sender_dict = {
        'key': "Total hosts",
        'value': thosts,
    }
    lines.append(sender_dict)

    output = __salt__['cmd.run']('icinga2 feature list')
    output_lines = output.split('\n')
    # output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_separated = [
        [i for i in x.split(': ') if i] for x in output_lines]

    for x in output_lines_separated:
        if not x:
            continue
        if type(x) == str:
            lines[-1]['error'] = x
        elif len(x) > 1:
            sender_dict = {
                'key': x[0],
                'value': x[1].replace(' ', ', '),
            }
            lines.append(sender_dict)

    try:
        f = __salt__['cmd.run']('cat /etc/ssmtp/ssmtp.conf')
    except:  # TODO use specific Exception typ
        f = ''
    ssmtp_data = ssmtp_to_dict(f)

    sender_dict = {
        'key': "Sending notifications from",
        'value': ssmtp_data.get('AuthUser', ''),
    }
    lines.append(sender_dict)

    sender_dict = {
        'key': "Mail server",
        'value': ssmtp_data.get('mailhub', ''),
    }
    lines.append(sender_dict)

    sender_dict = {
        'key': "Email password",
        'value': "Password is unconfigured/empty" if ssmtp_data.get('AuthPass', '') == 'empty' else "Password is configured/non-empty",
    }
    lines.append(sender_dict)

    return lines



def panel_history_summary_weekly(name,host_name):
    res=panel_history_summary(host_name,name,'1week')
    return res

def panel_history_summary_monthly(name, host_name):
    res=panel_history_summary(host_name,name,'1month')
    return res


def panel_history_summary(host_name='*', name='*', historyperiod='*'):
    data = get_hosts_periods_data(host = host_name, service = name, duration = historyperiod) or {host_name : {}}
    lines = []
    total_time = data[host_name].get('total')
    summary_dict = {
        'key': "Hostname",
        'value': host_name
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "Service",
        'value': name
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "Time in OK state",
        'value': pretty_time_and_percent(data[host_name].get('OK'),total_time)
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "Time in WARNING state",
        'value': pretty_time_and_percent(data[host_name].get('Warning'),total_time)
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "Time in CRITICAL state",
        'value': pretty_time_and_percent(data[host_name].get('Critical'),total_time)
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "Time in UNKNOWN state",
        'value': pretty_time_and_percent(data[host_name].get('Unknown'),total_time)
    }
    lines.append(summary_dict)

    summary_dict = {
        'key': "TOTAL TIME",
        'value': seconds_to_pretty(total_time) or '-'
    }
    lines.append(summary_dict)

    return lines

def pretty_time_and_percent(data, total):
    if data:
        text = '('+ "{0:05.2f}".format(data*100/total) + '%) '+ seconds_to_pretty(data)
    else:
        text = '-' 
        # text = '('+str(data*100/total)+'%) ' + seconds_to_pretty(data)
    return text

def panel_history_events_weekly(name, host_name):
    res=panel_history_events(host_name,name,'1week')
    return res

def panel_history_events_monthly(name, host_name):
    res=panel_history_events(host_name,name,'1month')
    return res


def panel_history_events(host_name='*', name='*', historyperiod='*'):
    host_data = get_history_data(duration = historyperiod, host_name = host_name, service_display_name = name)
    #We add this element to the list for calculating lengths - we iterate to the (i-1)th element and subtract timestamps
#    host_data.sort(key = lambda x: x['timestamp'], reverse = True)
    host_data = [{'timestamp' : int(time.time())}] + host_data
    timestamp_to_date = lambda t: datetime.datetime.fromtimestamp(int(t)).strftime('%Y-%m-%d %H:%M:%S')
    duration_to_pretty = lambda d: ' '.join(seconds_to_pretty(abs(int(d))).split(' ')[:2])

    data = [
        {
            'index' : i,
            'key' : timestamp_to_date(host_data[i]['timestamp']),
            'value' : states[int(host_data[i]['state'])], 
            'service' : host_data[i]['service_description'],
            'host' : host_data[i]['host_name'],
            'output' : host_data[i]['output'],
            'type' : host_data[i]['type'].split('_')[0],
            'state' : states[int(host_data[i]['state'])],
            'name': timestamp_to_date(host_data[i]['timestamp']),
            'duration' : duration_to_pretty(int(host_data[i]['timestamp']) - int(host_data[i-1]['timestamp'])),

        }
    for i in range(1, len(host_data))]

    return data

def ssmtp_to_dict(data):
    data = [x.strip() for x in data.split('\n') if x]

    data = [x for x in data if x[0] != '#' and '=' in x and x]
    data = dict([x.split('=') for x in data])
    return data


def edit_win_host_credentials(**kwargs): #standalone_user = '', standalone_password = '', domain_user = '', domain_password = ''):
    
    for conf_type in ['standalone', 'domain']: 
        conf_file = '/etc/icinga2/conf.d/cred_win_%s.txt' % conf_type

        new_data = {x.split('_')[1] : kwargs[x] for x in kwargs if conf_type in x}

        with open(conf_file, 'r') as f: 
            conf_data = f.read().split('\n')


        #We convert it from key=value to {"key" : "value"}
        conf_data = [x.split('=') for x in conf_data if x]
        conf_data = {x[0] : x[1] for x in conf_data}

        #We replace only the values which exist
        conf_data = {x : new_data.get(x, conf_data[x]) for x in conf_data}

        #And we convert it back to key=value
        conf_data = conf_data.items()
        conf_data = '\n'.join(['='.join(x) for x in conf_data]) + '\n'

        with open(conf_file, 'w') as f: 
            f.write(conf_data)

    return kwargs.get('standalone_user')


def add_win_host_to_icinga(host_name, displayname, always_on, joined, printer, mssql, iis):
    value_pairs = {"vars.os": "Windows"}
    if displayname:
        value_pairs["display_name"] = displayname
    else:
        displayname = host_name
        value_pairs["display_name"] = displayname

    if always_on == 'Yes':
        value_pairs["vars.windesktop"] = "False"
    else:
        value_pairs["vars.windesktop"] = "True"

    if joined == 'Domain Member':
        value_pairs["vars.standalone"] = "False"
        value_pairs["vars.domain_controller"] = "False"
    elif joined == 'Domain Controller':
        value_pairs["vars.standalone"] = "False"
        value_pairs["vars.domain_controller"] = "True"
    elif joined == 'Standalone':
        value_pairs["vars.standalone"] = "True"
        value_pairs["vars.domain_controller"] = "False"
        value_pairs["vars.wmi_authfile_path"] = "/etc/icinga2/conf.d/cred_win_standalone.txt"

# Different values depending on credentials set
    if joined == 'Standalone':

        if mssql == 'Yes':
            value_pairs["vars.mssql_server_standalone"] = "True"
        elif mssql == 'No':
            value_pairs["vars.mssql_server_standalone"] = "False"
        elif mssql == 'Express version':
            value_pairs["vars.mssql_server_standalone"] = "True"
            value_pairs["vars.mssql_edition"] = "Express"

        if printer == 'Yes':
            value_pairs["vars.printserver_standalone"]="True"
        else:
            value_pairs["vars.printserver_standalone"]="False"        
        if iis == 'Yes':
            value_pairs["vars.iis_server_standalone"]="True"
        else:
            value_pairs["vars.iis_server_standalone"]="False"            
    else:
        if mssql == 'Yes':
            value_pairs["vars.mssql_server"]="True"
        elif mssql == 'No':
            value_pairs["vars.mssql_server"]="False"
        elif mssql == "Express version":
            value_pairs["vars.mssql_server"]="True"
            value_pairs["vars.mssql_edition"]="Express"
            
        if printer == 'Yes':
            value_pairs["vars.printserver"]="True"
        else:
            value_pairs["vars.printserver"]="False"        
        if iis == 'Yes':
            value_pairs["vars.iis_server"]="True"
        else:
            value_pairs["vars.iis_server"]="False"   

    add_host_to_icinga(displayname, host_name, value_pairs)
    return value_pairs


def add_host_to_icinga(host_name, ip_address, value_pairs = {}):
    conf_dir='/etc/icinga2/conf.d/%s.conf' % host_name
    host_conf=icinga_conf_template % (host_name, ip_address)
    if value_pairs:
        for pair in value_pairs:
            host_conf += '\n  ' + pair + '="' + value_pairs[pair] + '"'
    host_conf += '\n}'
    with open(conf_dir, 'w') as f:
        f.write(host_conf)

    try:
        reload=subprocess.call(['service', 'icinga2', 'reload'])
    except:
        reload=True
    if reload:
        subprocess.check_output(['service', 'icinga2', 'restart'])
    return True

def icinga2_problems():
    out=subprocess.check_output(
        ['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out=json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts={}
    service_state_names={"0": "OK", "1": "Warning",
                        "2": "Critical", "3": "Unknown", '99': 'Pending'}
    for service_obj in json_out:
        host=service_obj['host_name']
        service={'name': service_obj['service_description'],
                'state': service_state_names[service_obj['service_state']],
                'output': service_obj['service_output']}
        if service['state'] != 'OK':
            if host in hosts:
                hosts[host].append(service)
            else:
                hosts[host]=[service]

    # Now the data is structured, but it has no schema (each host is a key)
    # We want to transform [{'host1': data}, ...] into [{'name': host1, data}, ...]
    # So that we have an API friendly result

    formatted_hosts=[]
    for host in hosts:
      
        formatted_hosts.append({'host_name': host, 'services': hosts[host]})
    result=sorted(formatted_hosts, key = lambda x: (
        x['host_name']), reverse=False)
    return result
    # return formatted_hosts #result


def icinga2_singlehost(host_name):
    out=subprocess.check_output(
        ['icingacli', 'monitoring', 'list', '--format', 'json', '--host='+host_name])
    json_out=json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts={}
    service_state_names={"0": "OK", "1": "Warning",
                        "2": "Critical", "3": "Unknown", '99': 'Pending'}
    for service_obj in json_out:
        host=service_obj['host_name']
        service={'name': service_obj['service_description'],
                'state': service_state_names[service_obj['service_state']],
                'output': service_obj['service_output']}
        if host in hosts:
            hosts[host].append(service)
        else:
            hosts[host]=[service]

    # Now the data is structured, but it has no schema (each host is a key)
    # We want to transform [{'host1': data}, ...] into [{'name': host1, data}, ...]
    # So that we have an API friendly result

    formatted_hosts=[]
    for host in hosts:
        formatted_hosts.append({'host_name': host, 'services': hosts[host]})
    result=sorted(formatted_hosts, key = lambda x: (
        x['host_name']), reverse=False)
    return result
    # return formatted_hosts #result


def icinga2():
    out=subprocess.check_output(
        ['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out=json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts={}
    service_state_names={"0": "OK", "1": "Warning",
                        "2": "Critical", "3": "Unknown", '99': 'Pending'}
    for service_obj in json_out:
        host=service_obj['host_name']
        service={'name': service_obj['service_description'],
                'state': service_state_names[service_obj['service_state']],
                'output': service_obj['service_output']}
        if host in hosts:
            hosts[host].append(service)
        else:
            hosts[host]=[service]

    # Now the data is structured, but it has no schema (each host is a key)
    # We want to transform [{'host1': data}, ...] into [{'name': host1, data}, ...]
    # So that we have an API friendly result

    formatted_hosts=[]
    for host in hosts:
        formatted_hosts.append({'host_name': host, 'services': hosts[host]})
    result=sorted(formatted_hosts, key = lambda x: (
        x['host_name']), reverse=False)
    return result
    # return formatted_hosts #result


def icinga2_summary():
    out=subprocess.check_output(
        ['icingacli', 'monitoring', 'list', '--format', 'json'])
    json_out=json.loads(out)

    # The data that we receive is flat, we want to group services by host.
    # hosts will be a dict that looks like: {'host1': [{'name': 'service1', 'state': 1}, ...], ...}
    hosts={}
    service_state_names={"0": "OK", "1": "Warning",
                        "2": "Critical", "3": "Unknown", '99': 'Pending'}
    for service_obj in json_out:
        host=service_obj['host_name']
        service={'name': service_obj['service_description'],
                'state': service_state_names[service_obj['service_state']],
                'output': service_obj['service_output']}
        if host in hosts:
            hosts[host].append(service)
        else:
            hosts[host]=[service]

    # Now the data is structured, but it has no schema (each host is a key)
    # We want to transform [{'host1': data}, ...] into [{'name': host1, data}, ...]
    # So that we have an API friendly result

    formatted_hosts=[]
    for host in hosts:
        count_ok=0
        count_warning=0
        count_critical=0
        count_unknown=0
        count_pending=0
        for services in hosts[host]:
            if services['state']=='OK':
                count_ok=count_ok+1
            if services['state']=='Warning':
                count_warning=count_warning+1
            if services['state']=='Critical':
                count_critical=count_critical+1
            if services['state']=='Unknown':
                count_unknown=count_unknown+1
            if services['state']=='Pending':
                count_pending=count_pending+1
        state='OK'
        if count_warning>0:
            state='Warning'
        if count_critical>0:
            state='Critical'
        if (count_unknown>0) and (count_critical==0) and (count_warning==0):
            state='Unknown'
        if (count_pending>0) and (count_critical==0) and (count_warning==0):
            state='Pending'
        if count_ok==0:
            count_ok=''
        if count_warning==0:
            count_warning=''
        if count_critical==0:
            count_critical=''
        if count_unknown==0:
            count_unknown=''
        if count_pending==0:
            count_pending=''

        formatted_hosts.append({'host_name': host, 'OK': count_ok, 'Warning' :count_warning,'Critical' :count_critical,'Unknown' :count_unknown,'Pending' :count_pending, 'state': state})
    result=sorted(formatted_hosts, key = lambda x: (
        x['host_name']), reverse=False)
    return result
    # return formatted_hosts #result

user = 'admin'
def seconds_to_pretty(seconds):
    periods = [
        ('Months', 12 * 7 * 24 * 60 * 60), 
        ('Weeks', 7 * 24 * 60 * 60),
        ('Days', 24 * 60 * 60),
        ('Hours', 60 * 60), 
        ('Minutes', 60), 
        ('Seconds', 1),
    ]

    result = ''
    for period in periods: 
        if seconds >= period[1]: 
            number_period = int(seconds / period[1])
            period_val = period[0] if number_period > 1 else period[0][:-1]
            seconds -= number_period * period[1]

            result += str(number_period) + ' ' + period_val + ' '

    return result

def get_hosts_in_history(history_data):
    return list(set([x['host_name'] for x in history_data]))

def remove_redundant_timestamps(history_data):
    data_temp = history_data[:]
    last_state = None
    for element in history_data: 
        if element['state'] == last_state: 
            data_temp.remove(element)
        else: 
            last_state = element['state']

    return data_temp


def get_state_periods(history_data):
    state_periods = [
        {
            'length' : int(history_data[i+1]['timestamp']) - int(history_data[i]['timestamp']), 
            'state' : history_data[i]['state'], 
            'host_name' : history_data[i]['host_name'],
            'service_name' : history_data[i]['service_display_name']
        } 
    for i in range(len(history_data)-1)]

    state_periods.append({'length' : time.time() - int(history_data[-1]['timestamp']), 'state' : history_data[-1]['state'], 'host_name' : history_data[-1]['host_name'], 'service_name' : history_data[-1]['service_display_name']})
    return state_periods


def get_total_times(history_data, host_name, service_name):
    state_periods = get_state_periods(history_data)

    total_times = { 
        states[i] : (sum([x['length'] for x in state_periods if int(x['state']) == i and x['host_name'] == host_name and x['service_name'] == service_name]))
    for i in range(len(states))}

    total_times['total'] = sum([x['length'] for x in state_periods])
    # total_times['total'] = (total_times['total_seconds'])


    return total_times

def get_history_for_host(history_data, host_name, service_name):
    host_data = [x for x in history_data if x['host_display_name'] == host_name]
    if not host_data: 
        raise Exception('No data found for host ' + str(host_name))

    host_data = sorted(host_data, key = lambda x: x['timestamp'])
    host_data = remove_redundant_timestamps(host_data)

    host_data = get_total_times(host_data, host_name, service_name)
    host_data['service'] = service_name
    host_data['host'] = host_name

    return host_data

def get_history_data(duration, host_name, service_display_name):
    headers = {'Accept' : 'application/json'}
    user_auth = auth=HTTPBasicAuth(user, get_password())

    params = {'host_display_name': host_name, 'modifyFilter' : '1', 'format' : 'json', 'service_display_name' : service_display_name} #'type!' : 'notification',

    url = 'http://%s/monitoring/list/eventhistory?type!=notify&timestamp>=-%s' % (get_ip(), duration)

    result = requests.get(url, headers = headers, auth = user_auth, params = params)
    result = result.json()
    result = [x for x in result if x.get('service_display_name')]

    return result

def get_hosts_periods_data(host, service, duration = '7days'):
    history_data = get_history_data(duration, host, service)
    hosts = get_hosts_in_history(history_data)

    hosts_histories = {h : get_history_for_host(history_data, h, service) for h in hosts}
    return hosts_histories


def force_check(service_name,host_name):
    out=subprocess.check_output(
        ['/usr/lib/nagios/plugins/force_check.sh', host_name, service_name])
#    json_out=json.loads(out)
    return "OK"
    # return formatted_hosts #result

