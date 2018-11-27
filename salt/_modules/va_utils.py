import salt, subprocess, json, importlib, sys, os, random, string, inspect, yaml
from va_salt_utils.va_pdf_utils import get_pdf
from salt.client import LocalClient


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

panel_jsons = {
#    'va_directory' : '/opt/va-directory/samba.json'
}

salt_panels = ''

error_msgs = ['Minion did not return. [Not connected]']

def __init__(opts):
# Init global
    global salt_panels
    salt_panels = __salt__

#Checks if a function is documented according to the VA standard
#Basically, if you want a function to show up when calling get_module_functions(), it needs to: 
#1. Have a __doc__ string
#2. Said doc string needs to be yaml-formatted
#3. It needs to be a dict
#4. It needs to have the 'description', 'output' and 'arguments' keys, alongside any other keys you want. 
#5. 'description' and 'output' are just strings, 'arguments' is a list of dictionaries, each dictionary having the name of the argument as a key and the description as a value. 
#You can check out the functions we've written to see how it should look. 

def function_is_documented(f):
    """
        description: Checks if a function is documented properly. In order for it to be so, it needs to have a __doc__ string which is yaml formatted, and it should be a dictionary with 'description', 'output' and 'arguments' keys, plus any others you want, where 'description' and 'output' are strings, and 'arguments' is a list of dictionaries where the key is the name of the argument, and the value is its description. 
        arguments: 
          - f: The function for whih the check is done
        output: Boolean, whether the function is formatted. 
        
    """
    doc = f.__doc__
    #Make sure doc is not empty
    if doc: 
        #Check if doc is yaml
        try: 
            doc = yaml.load(doc)
            #And dict
            if type(doc) == dict: 
                #It needs to have the 'description', 'output' and 'arguments' keys
                if all([x in doc.keys() for x in ['description', 'output', 'arguments']]):
                    #description and output should be strings, arguments should be a list of dictionaries. 
                    if type(doc['description']) == str and type(doc['output']) == str and type(doc['arguments']) == list and all([type(x) == dict for x in doc['arguments']]):
                        return True
        except yaml.parser.ParserError: 
            pass 
    return False

def get_documented_module_functions():
    """
        description: Returns all documented module functions. Documented functions are subject to some rules which can be seen in the function_is_documented() function documentation. 
        arguments: []
        output: A dictionary with module names as keys, and the value is a dictionary of all documented functions. Example: {"va_email" : {"list_users" : {"description" : "...", "output" : "...", "arguments" : [...]}, "add_user_ruls" : {...}}, ...}
    """
    all_functions = {}
    modules = ['va_backup', 'va_email', 'va_proxy']
    for module in modules: 
        imported_module = importlib.import_module(module)
        module_functions = inspect.getmembers(imported_module, inspect.isfunction)
        module_functions = [[x[0], yaml.load(x[1].__doc__)] for x in module_functions if function_is_documented(x[1])]
        all_functions[module] = module_functions

    return all_functions

def get_all_roles():
    cl = LocalClient()
    result = cl.cmd('*', 'grains.get', arg = ['role'])
    return {x : result[x] for x in result if result[x] not in error_msgs and result[x]}

def check_functionality():
    bash_cmd = '/usr/lib/nagios/plugins/check_functionality.sh'
    try:
        out = subprocess.check_output([bash_cmd])
        out = out.split('|')[0]
        returncode = [{"state":"OK", "output":out}]
    except subprocess.CalledProcessError as e:
        out = ''
        if e.returncode == 1:
            returncode = [{"state":"Warning", "output":e.output.split('|')[0]}]
        else:
            returncode = [{"state":"Critical", "output":e.output.split('|')[0]}]

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


def generate_password():
    result = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + str(".#^-_")) for _ in range(7))
    mustCaps = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(1))
    mustNum = ''.join(random.SystemRandom().choice(string.digits) for _ in range(1))
    mustChar = ''.join(random.SystemRandom().choice(str(".#^-_")) for _ in range(1))
    together = result+mustCaps+mustNum+mustChar
    mixed = ''.join(random.sample(together,len(together)))
    return mixed

def get_time_zone():
    result = __salt__['timezone.get_zone']()
    if not result: 
        raise Exception("Error")
    return result


def get_clock():
    result = __salt__['system.get_system_date_time']()+' - '+get_time_zone()
    if not result: 
        raise Exception("Error")
    return result

def get_ip_addresses():
    ips = __salt__['grains.get']('ipv4')
    if not ips: 
        raise Exception("Error")
    else:
        result = []
        for ip in ips:
            if ip != '127.0.0.1':
                result.append(ip)
    return result

def get_dns_addresses():
    result = __salt__['grains.get']('dns')['nameservers'] #('nameservers')
    if not result: 
        raise Exception("Error")
    return result

def panel_networking():
    result = [{"ip":get_ip_addresses(), "dns":get_dns_addresses(), "clock":get_clock()}]
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
    if module_name + '.get_panel' in salt_panels:

#        try:
        panel =  salt_panels[module_name + '.get_panel'](panel_name, *args, **kwargs)
#        except: 
#            panel = None
    if panel: 
        return panel

    module = importlib.import_module(module_name)
    if module_name in panel_jsons.keys():
        panel = json.load(open(panel_jsons[module_name]))
    else:
        panel = getattr(module, 'panels')
    panel = panel.get(panel_name)
    panel = parse_panel(panel, module_name, args, kwargs)
    return panel

def parse_panel(panel, module_name, args, kwargs):
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

