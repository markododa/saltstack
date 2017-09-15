# VPN

The VPN application is an OpenVPN server. OpenVPN accounts for external users can be created when creating a new user, through the "Apps / Active Directory / View/Add users", by selecting the "Use VPN" checkbox.

If an user has been created without the "Use VPN" option, new VPN certificate can be created through the "Apps / VPN / VPN Users" panel, using the "Add user" button. After a VPN key has been created for a user it can be downloaded from the "VPN Users" panel, through the control "Download certificate", for a particular user. Then the certificate file should be placed into the OpenVPN configuration directory of the client which is trying to connect. On a Windows system, this is typically "C:\Program files\OpenVPN\config" The certificate file includes the ca public certificate and the user's private and public keys.

User certificates can also be revoked, which will disable the user from future logins to the VPN server and to the private cloud.

Recommended folder for back-up is: /etc/openvpn/ (VPN credentials and configruaration)

Further documentation can be found in the [offical OpenVPN website](https://openvpn.net/index.php/open-source/documentation/howto.html)
