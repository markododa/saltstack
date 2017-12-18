import salt, os.path, subprocess, json, requests
from va_utils import check_functionality as panel_check_functionality

admin_user = 'admin'

try:
    admin_pass = __salt__['pillar.get']('credentials.admin_password')
except NameError: 
    #This happens when the module is first imported and the __salt__ dict is not instantiated. 
    admin_pass = '' 


panel={"owncloud.overview":{"title":"Overview","tbl_source":{"table_chkf":{"action":"panel_check_functionality","cols":["status","output"]},"table_plugins":{"action":"panel_plugins","cols":["plugin","status"]}},"content":[{"type":"Table","name":"table_chkf","reducers":["table","panel","alert"],"columns":[{"key":"status","label":"Status","width":"30%"},{"key":"output","label":"Value"}],"id":["status"],"source":"va_utils.check_functionality"},{"type":"Table","name":"table_plugins","reducers":["table","panel","alert"],"columns":[{"key":"plugin","label":"Plugin name","width":"30%"},{"key":"status","label":"Status"}],"id":["status"],"source":"panel_plugins"}]},"owncloud.users":{"title":"Users","tbl_source":{"table_users":{"action":"panel_list_users","cols":["name","username","lastlogin"]}},"content":[{"type":"Table","name":"table_users","reducers":["table","panel","alert"],"columns":[{"key":"username","label":"Username"},{"key":"name","label":"Name",},{"key":"lastlogin","label":"Last Login"}],"id":["username"],"source":"panel_list_users"}]},"owncloud.quotas":{"title":"Quotas","tbl_source":{"table_quota":{"action":"panel_quota","cols":["displayname","enabled","used","total"]}},"content":[{"type":"Table","name":"table_quota","reducers":["table","panel","alert"],"columns":[{"key":"displayname","label":"Name",},{"key":"enabled","label":"Enabled"},{"key":"used","label":"Used bytes"},{"key":"total","label":"Total bytes"}],"id":["displayname"],"source":"panel_quota"}]},"owncloud.shares":{"title":"Shares","tbl_source":{"table_shares":{"action":"panel_shares","cols":["displayname_owner","expiration","file_target","item_type","share_with"]}},"content":[{"type":"Table","name":"table_shares","reducers":["table","panel","alert"],"columns":[{"key":"displayname_owner","label":"Share Owner",},{"key":"expiration","label":"Expire"},{"key":"file_target","label":"Target"},{"key":"item_type","label":"Type"},{"key":"share_with","label":"Shared with"}],"id":["displayname"],"source":"panel_shares"}]}}

def bytes_to_readable(num, suffix='B'):
    """Converts bytes integer to human readable"""

    num = int(num)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#For some reason, using /shares or /users only gives you some information. You have to manually iterate through users or shares to get data like quota. This is done through salt for efficiency.
def panel_shares():
        url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares'
        params = {"format" : "json"}
        files = requests.get(url, params = params, verify = False).text
        files = json.loads(files)['ocs']['data']
        if not files : return []
        files_list = []
        for f in files:
                url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares/' + str(f['id']) + '?format=json'
                result = requests.get(url, verify = False).text
                new_file = json.loads(result)['ocs']['data']['element']
                files_list.append(new_file)
        return files_list

#For some reason, using /users only gives you the usernames. You have to manually retrieve all users using /users/getuser.
def panel_quota():
        url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/cloud/users'
        params = {"format" : "json"}
        users = requests.get(url, params = params, verify = False).text
        users = json.loads(users)['ocs']['data']['users']
        users_list = []
        for user in users:
                url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/cloud/users/'+user+'?format=json'
                new_user = requests.get(url, verify = False).text
                new_user =json.loads(new_user)
                new_user = new_user['ocs']['data']

                #We want the data from the user_quota to be on the same level as the rest of the data. 
                quota = new_user.pop('quota')
                quota = {
                    x : bytes_to_readable(quota[x])
                for x in quota}
                new_user.update(quota)
                users_list.append(new_user)

        return users_list


#def panel_check_functionality():
#    return [{"key":"1 goo"},{"key":"2 boo"}]


def panel_list_users():
    output =  __salt__['cmd.run']("sudo -u www-data /mnt/va-owncloud/owncloud/occ ldap:search ''")
    output_lines = output.split('\n')
#[1:-2]
    output_lines_stripped = [x.strip() for x in output_lines]
    output_lines_column_separated = [[i for i in x.split(' (') ] for x in output_lines_stripped]
    users = []
    for x in output_lines_column_separated:
        user_name=x[1].replace(')','')
        last_login= __salt__['cmd.run']("sudo -u www-data /mnt/va-owncloud/owncloud/occ user:lastseen "+user_name)
        user = {
            'name' : x[0],
            'username' : user_name,
            'lastlogin' : ''.join(last_login.split(': ')[1:]),
        }
        users.append(user)

    return users



def panel_plugins():
    output =  __salt__['cmd.run']("sudo -u www-data /mnt/va-owncloud/owncloud/occ app:list")
    output_lines = output.split('\n')[1:]
    output_lines_stripped = [x.strip() for x in output_lines]
    #output_lines_column_separated = [x.split(' (') for x in output_lines_stripped]
    users = []
    pstatus = "Enabled"
    for x in output_lines_stripped:
        if x == "Disabled:":
            pstatus="Disabled"
        else:
            pname = x[2:]
        user = {
            'plugin' : pname,
            'status' : pstatus,
        #    'Lastlogin' : ''.join(last_login.split(': ')[1:]),
        }
        users.append(user)

    return users



