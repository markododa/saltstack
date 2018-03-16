import os
import time, datetime
import subprocess, va_utils, json, re
from va_utils import check_functionality as panel_check_functionality
from va_proxy_panels import panels

proxy_conf_dir = '/etc/e2guardian'
config_line = '.Include</etc/e2guardian/lists/blacklists/{category}/domains>'

def e2guardian_reload():    
    try:
        reload=subprocess.call(['/usr/sbin/e2guardian', '-g'])
    except:
        reload=True
    if reload:
        subprocess.check_output(['/usr/sbin/e2guardian', '-r'])
    return True

def generate_config_line_for_cat(category):
    line = config_line.format(category = category)
    return line

def get_groups():
    e2_confs = [proxy_conf_dir + '/e2guardianf%s.conf' % (str(i)) for i in range(1, 4)]
    groups = []
    for conf in e2_confs:
        with open(conf) as f: 
            c = f.read()
        c = c.split('\n')
        group_name = [x for x in c if 'groupname' in x and '#' not in x][0]
        group_name = group_name.split(' = ')[1]
        group_name = group_name.replace("'", '')
        groups.append(group_name)
    return groups


def get_config_file_path_for_group(group, conf_type):
    groups = get_groups()
    configs = {
        'banned_site_list' : proxy_conf_dir + '/lists/bannedsitelist%s',
        'exception_site_list' : proxy_conf_dir + '/lists/exceptionsitelist%s',
        'e2_guardian' : proxy_conf_dir + '/e2guardianf%s.conf',
    }
    conf = configs.get(conf_type)
    conf = conf % (groups.index(group) + 1)
    return conf

def get_config_file_for_group(group, conf_type):
    conf_path = get_config_file_path_for_group(group, conf_type)

    with open(conf_path) as f: 
        result = f.read()

    return result

def write_config_file_for_group(group, conf_type, new_data):
    
    conf_path = get_config_file_path_for_group(group, conf_type)

    with open(conf_path, 'w') as f:
        f.write(new_data)
   


def get_all_categories():
    categories = os.listdir(proxy_conf_dir + '/lists/blacklists')
    return categories


def get_banned_list(group):
    conf_file = get_config_file_for_group(group, 'banned_site_list')
    conf_file = conf_file.split('\n')

    includes = [x for x in conf_file if 'Include' in x and '#' not in x]
    bans = [x for x in conf_file if 'Include' not in x and '#' not in x and x]

    all_categories = get_all_categories()

    included = [x for x in all_categories if any([x in i for i in includes])]
    excluded = [x for x in all_categories if x not in included]

    result = {'included' : included, 'bans' : bans, 'excluded' : excluded}

    return result


def panel_banned_list():
    groups = get_groups()
    all_bans = []
    for g in groups: 
        conf_file = get_config_file_for_group(g, 'banned_site_list')
        conf_file = conf_file.split('\n')
        all_bans += [{'group': g,'item' : x } for x in conf_file if 'Include' not in x and '#' not in x and x]
# all_exceptions += get_exceptions_list(g)
    return all_bans 

def category_to_line(category) : 
    if 'Include' in category: return category
    line_template = '.Include</etc/e2guardian/lists/blacklists/%s/domains>'
    category_line = line_template % category
    return category_line

def manage_site_bans(group, value, ban_type = 'bans', action = 'append'):
    l = get_banned_list(group)

    # print ('My l is : ', l, ' and adding : ', value)
    getattr(l[ban_type], action)(value)
    l['included'] = [category_to_line(x) for x in l['included']]

    conf_contents = '\n'.join(l['bans']) + '\n' + '\n'.join(l['included'])

    conf_file = get_config_file_path_for_group(group, 'banned_site_list')

    with open(conf_file, 'w') as f: 
        f.write(conf_contents)

    e2guardian_reload()
    
def add_customlist(item):
    manage_file_add(proxy_conf_dir + '/lists/blacklists/_custom/domains', item)


def remove_customlist(item):
    manage_file_remove(proxy_conf_dir + '/lists/blacklists/_custom/domains', item)


def manage_file_add(file,item):
    #NINO
    #write to file
    e2guardian_reload()
    return "Item added to file"

def manage_file_remove(file,item):
    #NINO
    #find and remove line
    e2guardian_reload()
    return "Item removed from file"

def panel_custom_list():
    conf_file = proxy_conf_dir + '/lists/blacklists/_custom/domains'
    with open(conf_file) as f: 
        conf_file = f.read()

    conf_file = conf_file.split('\n')

    result = [{'item': x } for x in conf_file if '#' not in x and x]
    
    return result

def add_extension(extension):
    manage_file_add(proxy_conf_dir + '/lists/exceptionextensionlist', item)

def remove_extension(extension):
    manage_file_remove(proxy_conf_dir + '/lists/exceptionextensionlist', item)

def add_exception_site(group, site):
    #NINO
    manage_site_bans(group, site, 'bans')
    #reload

def remove_exception_site(group, site):
    #NINO
    manage_site_bans(group, site, action = 'remove')
    #erload

def add_banned_site(group, site):
    manage_site_bans(group, site, 'bans')

def remove_banned_site(group, site):
    manage_site_bans(group, site, action = 'remove')

def add_banned_category(group, category):
    manage_site_bans(group, category, ban_type = 'included')

def remove_banned_category(group, category):
    manage_site_bans(group, category, ban_type = 'included', action = 'remove')

def get_exceptions_list(group):
    conf_file = get_config_file_for_group(group, 'exception_site_list')
    conf_file = conf_file.split('\n')

    result = [{'group': group, 'item' : x} for x in conf_file if '#' not in x and x]

    return result

def panel_exceptions_list():
    groups = get_groups()
    
    all_exceptions = []
    for g in groups: 
        all_exceptions += get_exceptions_list(g)
    return all_exceptions

def get_all_banned_lists():
    groups = get_groups()

    categories = get_all_categories()

    all_lists = {g : get_banned_list(g) for g in groups}

    cats = [{'category' : cat}  for cat in categories]
    cat_status_in_group = lambda cat, group: 'Denied' * (row['category'] in all_lists[group]['included']) + ' ' * (row['category'] in all_lists[group]['excluded'])
    [row.update({group : cat_status_in_group(cat, group) for group in groups}) for row in cats]
    result = sorted(cats, key = lambda x: x['category'], reverse = False)
    return result

def panel_statistics():
    #tail -n 100 /var/log/e2guardian/dstats.log
    #time		childs 	busy	free	wait	births	deaths	conx	conx/s
    #1521091807	20	0	20	0	0	0	0	0
    # ponekogash se pojavuva linija so headers/text
    # res = [{'time': '3434', 'childs': '2', 'busy': '3' , 'free': '6', 'wait': '3', 'births': '33', 'deaths': '22', 'conx': '32', 'conx/s': '1'}]
    # return res
    conf_file = '/var/log/e2guardian/dstats.log'
    with open(conf_file) as f: 
        conf_file = f.read()
    conf_file = conf_file.split('\n')
    conf_file = [x.split('\t') for x in conf_file if 'time' not in x and x][-140:]

    result = [{
        'time': to_time_string(x[0]), 
        'childs': x[1], 
        'busy': x[2], 
        'free': x[3], 
        'wait': x[4], 
        'births': x[5], 
        'deaths': x[6], 
        'conx': x[7], 
        'conx/s': x[8]
        } for x in conf_file ]
    
    return result

def to_time_string(timestamp):
    res = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
    return res

def panel_exceptions_extensions():
    conf_file = proxy_conf_dir + '/lists/exceptionextensionlist'
    with open(conf_file) as f: 
        conf_file = f.read()

    conf_file = conf_file.split('\n')

    result = [{'extension': x } for x in conf_file if '#' not in x and x]
    
    return result

def panel_ip_groups():
    #NINO
    # result = [{'group': 'VIP', 'range': '192.168.10.0-192.168.10.200' }]
    conf_file = proxy_conf_dir + '/lists/authplugins/ipgroups'
    with open(conf_file) as f: 
        conf_file = f.read()
    translate = conf_file.replace('filter1', 'Standard')
    conf_file = conf_file.split('\n')
    
    result = [{'range': x.split(' = ')[0], 'group': x.split(' = ')[1].replace('filter1', 'Standard').replace('filter2', 'VIP').replace('filter3', 'Safe')} for x in conf_file if '#' not in x and '=' in x]
    # result = [{'range': x.split(' = ')[0] , 'group': x.split(' = ')[1]} for x in conf_file if '#' not in x and x]

    return result

def action_edit_ip_group(group,range,new_range):
    #NINO
    return result


def action_remove_ip_group(group,range):
    #NINO
    return result


def action_add_ip_group(group,range):
    #NINO
    return result


def toggle_vip(category):
    toggle_cat=category
    res = toggle_category_status_in_group('VIP', toggle_cat)
    
def toggle_standard(category):
    toggle_cat=category
    res = toggle_category_status_in_group('Standard', toggle_cat)
    
def toggle_safe(category):
    toggle_cat=category
    res = toggle_category_status_in_group('Safe', toggle_cat)
    

def toggle_category_status_in_group(group, category):
    conf_file = get_config_file_for_group(group, 'banned_site_list')
    conf_file = conf_file.split('\n')

    category_line = [x for x in conf_file if category in x]

    if not category_line: 
        category_line = '#' + generate_config_line_for_cat(category)
        conf_file.append(category_line)
    else: 
        category_line = category_line[0]

    category_index = conf_file.index(category_line)
    
    #Cannot resist urge to codegolf...
    #It works but not pretty code. 
    #category_line = (category_line[0] != '#') * ('#' + category_line) + (category_line[0] == '#') * category_line[1:]

    if category_line[0] == '#': 
        category_line = category_line[1:]
    else: 
        category_line = '#' + category_line

    conf_file[category_index] = category_line
    conf_file = '\n'.join(conf_file)

    write_config_file_for_group(group, new_data = conf_file, conf_type = 'banned_site_list')
    
    e2guardian_reload()