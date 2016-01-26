import salt, os.path, subprocess, json

#For some reason, using /shares or /users only gives you some information. You have to manually iterate through users or shares to get data like quota. This is done through salt for efficiency. 
def owncloud_shares():
	url = 'http://admin:tezokpass@localhost/owncloud/ocs/v1.php/apps/files_sharing/api/v1/shares?format=json'
	files = subprocess.check_output(['curl',url])
	files = json.loads(files)['ocs']['data']
	if not files : return []
	files_list = []
	for file in files:
		new_file = json.loads(subprocess.check_output(['curl', 'http://admin:tezokpass@localhost/owncloud/ocs/v1.php/apps/files_sharing/api/v1/shares/' + str(file['id']) + '?format=json']))['ocs']['data']['element']
		files_list.append(new_file)
	return files_list

#For some reason, using /users only gives you the usernames. You have to manually retrieve all users using /users/getuser. 
def owncloud_users():
	url = 'http://admin:tezokpass@localhost/owncloud/ocs/v1.php/cloud/users?format=json'
	users = json.loads(subprocess.check_output(['curl', url]))['ocs']['data']['users']
	users_list = []
	for user in users:
		new_user =json.loads( subprocess.check_output(['curl', 'http://admin:tezokpass@localhost/owncloud/ocs/v1.php/cloud/users/'+user+'?format=json']))
		new_user = new_user['ocs']['data']
		users_list.append(new_user)
	return users_list
