import salt, vpn_parser

def add_user(username):
	result =  __salt__['cmd.retcode']('/etc/openvpn/easyrsa/easyrsa build-client-full '+username+' nopass',cwd='/etc/openvpn/easyrsa')
	return result == 0

def revoke_user(username):
	if __salt__['cmd.retcode']('echo yes | /etc/openvpn/easyrsa/easyrsa revoke '+username,cwd='/etc/openvpn/easyrsa',python_shell=True) == 0:
		__salt__['cmd.run']('/etc/openvpn/easyrsa/easyrsa gen-crl',cwd='/etc/openvpn/easyrsa')
                __salt__['cmd.run']('cp /etc/openvpn/easyrsa/pki/crl.pem /etc/openvpn/')
                __salt__['cmd.run']('chown nobody:nogroup /etc/openvpn/crl.pem')
		return True
	else:
		return False

def list_users():
	certs = open('/etc/openvpn/easyrsa/pki/index.txt', 'r')
	next(certs)
	active = []
	revoked = []
	for line in certs:
		if line[:1] == 'V':
			active = active + [line.split('CN=')[1].strip()]
		elif line[:1] == 'R':
			revoked = revoked + [line.split('CN=')[1].strip()]
	return {'active' : active, 'revoked' : revoked}

def get_config(username):
	config = open('/etc/openvpn/client.conf','r').read()
	ca = open('/etc/openvpn/easyrsa/pki/ca.crt', 'r').read()
	cert = open('/etc/openvpn/easyrsa/pki/issued/'+username+'.crt','r').read().split('-----BEGIN CERTIFICATE-----\n')[1]
	key = open('/etc/openvpn/easyrsa/pki/private/'+username+'.key','r').read()
	return config+'\n<ca>\n'+ca+'</ca>'+'\n<cert>\n-----BEGIN CERTIFICATE-----\n'+cert+'</cert>\n'+'<key>\n'+key+'</key>'

def get_status():
	return vpn_parser.open_and_parse_log('/run/openvpn/openvpn-status.log')

def list_user_logins(user):
        return vpn_parser.get_logins_for_user(user) 
