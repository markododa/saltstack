import salt

def add_user(username):
	if __salt__['cmd.retcode']('/etc/openvpn/easyrsa build-client-full '+username+' nopass',cwd='/etc/openvpn') == 0:
		return True
	else:
		return False

def revoke_user(username):
	if __salt__['cmd.retcode']('echo yes | /etc/openvpn/easyrsa revoke '+username,cwd='/etc/openvpn',python_shell=True) == 0:
		__salt__['cmd.run']('/etc/openvpn/easyrsa gen-crl',cwd='/etc/openvpn')
		return True
	else:
		return False

def list_users():
	certs = open('/etc/openvpn/pki/index.txt', 'r')
	next(certs)
	active = ''
	revoked = ''
	for line in certs:
		if line[:1] == 'V':
			active = active + 'Active: ' + line.split('CN=')[1]
		elif line[:1] == 'R':
			revoked = revoked + 'Revoked: ' + line.split('CN=')[1]
	return active+revoked

def get_config(username):
	config = open('/etc/openvpn/client.conf','r').read()
	ca = open('/etc/openvpn/pki/ca.crt', 'r').read()
	cert = open('/etc/openvpn/pki/issued/'+username+'.crt','r').read().split('-----BEGIN CERTIFICATE-----\n')[1]
	key = open('/etc/openvpn/pki/private/'+username+'.key','r').read()
	return config+'\n<ca>\n'+ca+'</ca>'+'\n<cert>\n-----BEGIN CERTIFICATE-----\n'+cert+'</cert>\n'+'<key>\n'+key+'</key>'

def get_status():
	return open('/run/openvpn/openvpn-status.log','r').read()
