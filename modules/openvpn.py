import salt

def add_user(username):
	__salt__['cmd.run']('/etc/openvpn/easyrsa build-client-full '+username+' nopass',cwd='/etc/openvpn')

def revoke_user(username):
	__salt__['cmd.run']('echo yes | /etc/openvpn/easyrsa revoke '+username,cwd='/etc/openvpn',python_shell=True)
	__salt__['cmd.run']('/etc/openvpn/easyrsa gen-crl',cwd='/etc/openvpn')
