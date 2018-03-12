import os

proxy_conf_dir = '/etc/e2guardian'

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
    excluded = [x for x in all_categories if x not in includes]

    result = {'included' : included, 'bans' : bans, 'excluded' : excluded}

    return result


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

    result = [x for x in conf_file if '#' not in x and x]

    return result


def get_all_banned_lists():
    groups = get_groups()

    all_lists = { 
        g : {
            'banned_site_list' : get_banned_list(g),
            'exception_site_list' : get_exceptions_list(g)
        } for g in groups
    }

    return all_lists    

def get_exceptions_extensions():
    conf_file = proxy_conf_dir + '/lists/exceptionextensionlist'
    with open(conf_file) as f: 
        conf_file = f.read()

    conf_file = conf_file.split('\n')

    result = [x for x in conf_file if '#' not in x and x]
    
    return result
