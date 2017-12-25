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

panel_check_functionality = check_functionality

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

def get_pdf(panel, pdf_file = '/tmp/table.pdf', range_from = 0):
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.pagesizes import letter, inch

    if range_from: return
    pdf_contents = {
        'title' : 'Some title',
        'tables' : [],
    }

    for table in panel['tbl_source']:
        panel_table = [x for x in panel['content'] if x.get('name') == table]
        columns = []
        if panel_table:
            panel_table = panel_table[0]
            columns = [x['label'] for x in panel_table['columns']]
        pdf_contents['tables'].append({'table' : panel['tbl_source'][table], 'name' : table, 'columns' : columns})

    elements = contents_to_elements(pdf_contents, pdf_file)
 
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    doc.build(elements)
  

def contents_to_elements(pdf_contents, pdf_file):
    from reportlab.lib import colors
    from reportlab.platypus import Table, TableStyle


    #    elements = [pdf_contents['title']]
    elements = []
    for table in pdf_contents['tables']:
#        elements.append(table['name'])
        columns = table['table'][0].keys()
        columns = table.get('columns', columns)

        data = [columns]
        for row in table['table']:
            for x in row: 
                row[x] = str(row[x]) #TODO properly convert lists to string

            data.append(row.values())

            pdf_table=Table(data)
            pdf_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

        elements.append(pdf_table)

    return elements

def get_panel_data_for_table(table, module_name, *args, **kwargs):
    table_cols = table.get('cols')
    table_args = table.get('args', [])
    table_module = table.get('module', module_name)

    panel_func =  __salt__[table_module + '.' + table['action']]

    panel_kwargs = {x : kwargs[x] for x in table_args}
    panel_data = panel_func(*args, **panel_kwargs)

    return panel_data


def get_content_data_for_modal(content_source, module_name, *args, **kwargs):
    content_args = content_source.get('args', [])
    content_module = content_source.get('module', module_name)
    positional_args = content_source.get('positional_args', 0)

    content_func = __salt__[content_module + '.' + content_source['action']]
    content_kwargs = {x : kwargs[x] for x in content_args}
    content_args = args[:positional_args]
#    content_data = content_func(*content_args, **content_kwargs)

    return content_data

def get_panel(module_name, panel_name, *args, **kwargs):
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
        panel_data = get_panel_data_for_table(table, module_name, *args, **kwargs)

        panel_data = [{i : x.get(i, '') for i in table.get('cols', [])} for x in panel_data]
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
