import salt, subprocess, json, importlib, sys, os
from va_pdf_utils import get_pdf

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

panel_jsons = {
#    'va_directory' : '/opt/va-directory/samba.json'
}

def check_functionality():
    bash_cmd = '/usr/lib/nagios/plugins/check_functionality.sh'
    try:
        out = subprocess.check_output([bash_cmd])
        out = out.split('|')[0]
        returncode = [{"status":"OK", "output":out}]
    except subprocess.CalledProcessError as e:
        out = ''
        if e.returncode == 1:
            returncode = [{"status":"WARNING", "output":e.output.split('|')[0]}]
        else:
            returncode = [{"status":"CRITICAL", "output":e.output.split('|')[0]}]

    return returncode

panel_check_functionality = check_functionality


def restart_functionality(status):
    bash_cmd = '/usr/lib/nagios/plugins/restart_functionality.sh'
    try:
        out = subprocess.check_output([bash_cmd])
        out = out.split('|')[0]
        returncode = "Restarting services was OK"
    except subprocess.CalledProcessError as e:
        out = ''
        if e.returncode == 1:
            returncode = "Problem with service configuration, aborting restart"
        else:
            returncode = "Restarting services was NOT successful"

    return returncode


def get_time_zone():
    result = __salt__['timezone.get_zone']()
    if not result: 
        raise Exception("Error")
    return result

def get_ip_addresses():
    result = __salt__['grains.get']('ipv4')
    if not result: 
        raise Exception("Error")
    return result

def get_dns_addresses():
    result = __salt__['grains.get']('dns')['nameservers'] #('nameservers')
    if not result: 
        raise Exception("Error")
    return result

def panel_networking():
    result = [{"ip":get_ip_addresses(), "dns":get_dns_addresses()}]
    return result


def get_panel_data_for_table(table, module_name, *args, **kwargs):
    table_args = table.get('args', [])
    table_module = table.get('module', module_name)

    panel_func =  __salt__[table_module + '.' + table['source']]

    panel_kwargs = {x : kwargs[x] for x in table_args}
    panel_data = panel_func(*args, **panel_kwargs)
    #TODO maybe properly check columns and get data as needed. 
#    panel_data = [{i : x.get(i, '') for i in table_columns} for x in panel_data]

    return panel_data


def get_content_data_for_modal(content_source, module_name, *args, **kwargs):
    content_args = content_source.get('args', [])
    content_module = content_source.get('module', module_name)
    positional_args = content_source.get('positional_args', 0)

    content_func = __salt__[content_module + '.' + content_source['source']]
    content_kwargs = {x : kwargs[x] for x in content_args}
    content_args = args[:positional_args]
#    content_data = content_func(*content_args, **content_kwargs)

    return content_data

def get_panel(module_name, panel_name, *args, **kwargs):
    #If the module already has a get_panel function, we just return that. 
    panel = None
    kwargs = {x : kwargs[x] for x in kwargs if x[0] != '_'}
    if module_name + '.get_panel' in __salt__:

#        try:
        panel =  __salt__[module_name + '.get_panel'](panel_name, *args, **kwargs)
#        except: 
#            panel = None
    if panel: 
        return panel

    module = importlib.import_module(module_name)
    if module_name in panel_jsons.keys():
        panel = json.load(open(panel_jsons[module_name]))
    else:
        panel = module.panels
    panel = panel.get(panel_name)
    temp_data = []
    for t in panel['tbl_source']:
        table = panel['tbl_source'][t]
        panel_data = get_panel_data_for_table(table, module_name, *args, **kwargs)
        panel['tbl_source'][t] = panel_data

    modals = [x.get('modals') for x in panel['content'] if x.get('modals')] or []
    for m in modals: 
        for modal_name in m: 
            for content in m[modal_name].get('content', []):
                if 'form_source' in content.keys():
                    content_source = content['form_source']
#                    content_data = get_content_data_for_modal(content_source, module_name, *args, **kwargs)
#                    for element in content: 
#                        element['value'] = content_data.get(element['name'], 'key not found')
            

    return panel
