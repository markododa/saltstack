import salt, subprocess, json, importlib, sys, os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

panel_jsons = {
    'va_directory' : '/opt/va-directory/samba.json'
}

def check_functionality():
    bash_cmd = '/usr/lib/nagios/plugins/check_functionality.sh'
    try:
        out = subprocess.check_output([bash_cmd])
        returncode = [{"status":"OK", "output":out}]
    except subprocess.CalledProcessError as e:
        out = ''
        if e.returncode == 1:
            returncode = [{"status":"WARNING", "output":e.output}]
        else:
            returncode = [{"status":"CRITICAL", "output":e.output}]

    return returncode

def get_panel(module_name, panel_name, *args):
    #If the module already has a get_panel function, we just return that. 
    panel = None
    if module_name + '.get_panel' in __salt__:
        try:
            panel =  __salt__[module_name + '.get_panel'](panel_name, *args)
        except: 
            panel = None

    if panel: 
        return panel

    module = importlib.import_module(module_name)
    if module_name in panel_jsons.keys():
        panel = json.load(open(panel_jsons[module_name]))
    else:
        panel = module.panel

    panel = panel.get(panel_name)


    for t in panel['tbl_source']:
        table = panel['tbl_source'][t]
        table_cols = table.get('cols')
        table_args = table.get('args', [])

        panel_func =  __salt__[module_name + '.' + table['action']]

        panel_kwargs = {x : kwargs[x] for x in table_args}
        panel_data = panel_func(**panel_kwargs)
        if table_cols:
            panel_data = [{i : x.get(i, '') for i in table_cols} for x in panel_data]
        panel['tbl_source'][t] = panel_data

    return panel
