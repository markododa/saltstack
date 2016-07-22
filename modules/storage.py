import salt, os.path, subprocess, json

admin_user = 'admin'
admin_pass = '1e5988624dd8973084f5'

#For some reason, using /shares or /users only gives you some information. You have to manually iterate through users or shares to get data like quota. This is done through salt for efficiency.
def owncloud_shares():
        url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares?format=json'
        files = subprocess.check_output(['curl', '-k', url])
        files = json.loads(files)['ocs']['data']
        if not files : return []
        files_list = []
        for file in files:
                url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/apps/files_sharing/api/v1/shares/' + str(file['id']) + '?format=json'
                file = subprocess.check_output(['curl', '-k', url])
                new_file = json.loads(file)['ocs']['data']['element']
                files_list.append(new_file)
        return files_list

#For some reason, using /users only gives you the usernames. You have to manually retrieve all users using /users/getuser.
def owncloud_users():
        url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/cloud/users?format=json'
        users = subprocess.check_output(['curl', '-k', url])
        users = json.loads(users)['ocs']['data']['users']
        users_list = []
        for user in users:
                url = 'https://' + admin_user + ':' + admin_pass + '@localhost/ocs/v1.php/cloud/users/'+user+'?format=json'
                new_user =  subprocess.check_output(['curl', '-k', url])
                new_user =json.loads(new_user)
                new_user = new_user['ocs']['data']
                users_list.append(new_user)
        return users_list


