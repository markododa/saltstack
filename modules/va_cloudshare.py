import salt, os.path, subprocess, json, requests, MySQLdb
from va_utils import check_functionality as panel_check_functionality
from va_cloudshare_panels import panels

admin_user = 'admin'

def get_admin_pass():
    admin_pass = __salt__['pillar.get']('admin_password')
    if not admin_pass: 
        raise Exception("admin_password from pillar is empty - can not perform authorized requests. ")
    return admin_pass


def bytes_to_readable(num, suffix='B'):
    """Converts bytes integer to human readable"""

    num = int(num)
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#For some reason, using /shares or /users only gives you some information. You have to manually iterate through users or shares to get data like quota. This is done through salt for efficiency.
def panel_shares():
    #TODO testing, remove these
        url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares'
        params = {"format" : "json"}
        files = requests.get(url, params = params, verify = False).text
        files = json.loads(files)['ocs']['data']
        if not files : return []
        files_list = []
        for f in files:
                url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares/' + str(f['id']) + '?format=json'
                result = requests.get(url, verify = False).text
                new_file = json.loads(result)['ocs']['data']['element']
                if f.has_key('url'):
                    #if (new_file['share_with'] == None) :
                    new_file['share_with'] = 'Direct link'
                    #    new_file['share_with'] = f['url'] #'link'
                    #else:
                    #    new_file['share_with'] = str(new_file['share_with'])+' + link'


                files_list.append(new_file)

        return files_list

def panel_new():
    #TODO testing, remove these
#        admin_user = 'vavo'
#        get_admin_pass = lambda: 'Qwert~12'
        url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares'
        params = {"format" : "json"}
        files = requests.get(url, params = params, verify = False).text
        files = json.loads(files)['ocs']['data']
        if not files : return []
        files_list = []
        for f in files:
                url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares/' + str(f['id']) + '?format=json'
                result = requests.get(url, verify = False).text
                new_file = json.loads(result)['ocs']['data']['element']
                if f.has_key('url'):
                    #if (new_file['share_with'] == None) :
                    new_file['share_with'] = 'Direct link'
                    #    new_file['share_with'] = f['url'] #'link'
                    #else:
                    #    new_file['share_with'] = str(new_file['share_with'])+' + link'


                files_list.append(new_file)

        return url

#For some reason, using /users only gives you the usernames. You have to manually retrieve all users using /users/getuser.
def panel_quota1():
    #Connecting to the database
    defaut_quota = get_defaut_quota()
    db = MySQLdb.connect("localhost","root","","owncloud")
    cursor = db.cursor()
    getid = "SELECT userid,configvalue FROM owncloud.preferences WHERE configkey='quota';"
    try:
        cursor.execute(getid)
        quotas = cursor.fetchall()
        addressbookid = address[0]
    except:
        pass 
    result = []
    for q in quotas:
        # user=q[0]
        # qouta=q[1]
        result.append({'user': q[0], 'quota': q[1]});
    db.close()
    return result


def user_quota(user,default_q):
    #Connecting to the database
    # defaut_quota = get_defaut_quota()
    db = MySQLdb.connect("localhost","root","","owncloud")
    cursor = db.cursor()
    getid = "SELECT userid,configvalue FROM owncloud.preferences WHERE userid=\'"+user+"\' AND configkey='quota';"
    try:
        cursor.execute(getid)
        quotas = cursor.fetchone()
        quota = quotas[1].replace(' ', '')
    except:
        quota = default_q 
    db.close()
    return quota


#def panel_check_functionality():
#    return [{"key":"1 goo"},{"key":"2 boo"}]


def panel_quota():
        url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/cloud/users'
        params = {"format" : "json"}
        users = requests.get(url, params = params, verify = False).text
        users = json.loads(users)['ocs']['data']['users']
        users_list = []
        default_q = get_defaut_quota()
        for user in users:
                url = 'http://' + admin_user + ':' + get_admin_pass() + '@localhost/ocs/v1.php/cloud/users/'+user+'?format=json'
                new_user = requests.get(url, verify = False).text
                new_user =json.loads(new_user)
                new_user = new_user['ocs']['data']

                #We want the data from the user_quota to be on the same level as the rest of the data. 
                quota = new_user.pop('quota')
                quota = {
                    x : bytes_to_readable(quota[x])
                for x in quota}
                new_user.update(quota)
                new_user['total'] = user_quota(user,default_q+" *")
                new_user['username'] = user
                users_list.append(new_user)

        return users_list



def panel_list_users():
# This will get only LDAP users, ight be better if we can list all of them	
    output =  __salt__['cmd.run']("sudo -u www-data /var/www/owncloud/occ ldap:search ''")
    output_lines = output.split('\n')
#[1:-2]
    output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_column_separated = [[i for i in x.split(' (') ] for x in output_lines_stripped]
    users = []
    for x in output_lines_column_separated:
        user_name=x[1].replace(')','')
        last_login= __salt__['cmd.run']("sudo -u www-data /var/www/owncloud/occ user:lastseen "+user_name)
        last_login = ''.join(last_login.split(': ')[1:]) or 'Never' #last_login
        user = {
            'name' : x[0],
            'username' : user_name,
            'lastlogin' : last_login,
        }
        users.append(user)

    return users

def action_setquota(username,storage_quota):
    # curl -X PUT http://admin:Qwert~123@localhost/ocs/v1.php/cloud/users/staci -d key="quota" -d value="100MB"
    return "Function not implemented yet! "+username+"/"+storage_quota

def get_defaut_quota():
    default_quota = " "
    db = MySQLdb.connect("localhost","root","","owncloud")
    cursor = db.cursor()

    getid = "SELECT configvalue FROM owncloud.appconfig WHERE configkey = 'default_quota';"
    try:
        cursor.execute(getid)
        default_quota = cursor.fetchone()
        default_quota = default_quota[0].replace(' ', '')
    except:
        default_quota = "none"

    db.close()

    return default_quota



def panel_plugins():
    output =  __salt__['cmd.run']("sudo -u www-data /var/www/owncloud/occ app:list")
    output_lines = output.split('\n')[1:]
    output_lines_stripped = [x.strip() for x in output_lines]
    #output_lines_column_separated = [x.split(' (') for x in output_lines_stripped]
    plugins = []
    pstatus = "Enabled"
    for x in output_lines_stripped:
        if x == "Disabled:":
            pstatus="Disabled"
        else:
            pname = x[2:]
            plugin = {
            'plugin' : pname,
            'status' : pstatus,
            }
            plugins.append(plugin)
    result = sorted(plugins, key = lambda x: (x['plugin']), reverse = False)
    return result



def panel_statistics():
    diskusage =__salt__['disk.usage']()[__salt__['cmd.run']('findmnt --target /var/www/owncloud/ -o TARGET').split()[1]]
    statistics = [{'key' : 'Storage partition used size (MB)', 'value': int(diskusage['used'])/1024},
                    {'key' : 'Storage partition free space (MB)', 'value': int(diskusage['available'])/1024},
                    {'key' : 'Storage partition mount point', 'value': diskusage['filesystem']},
                    {'key' : 'Limit per user', 'value': get_defaut_quota()}
                ]
    return statistics

def action_toggle_app(app,current_state):
    app=app.split(":")[0]
    cmd =""
    #return app
    if current_state == "Enabled":
        cmd= __salt__['cmd.run']("sudo -u www-data /var/www/owncloud/occ app:disable "+app)
    elif current_state == "Disabled":
        cmd= __salt__['cmd.run']("sudo -u www-data /var/www/owncloud/occ app:enable "+app)
    return
