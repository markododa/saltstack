# See https://openvpn.net/index.php/open-source/documentation/howto.html#examples
# for configuration details
# Important: Replace all '-' in names on left side with '_'!
{% import_yaml '/srv/pillar/credentials.sls' as credentials %}
# Defaults can be overwritten, see openvpn/map.jinja for default values
# openvpn:
#   lookup:
#     dh_files: ['4096'] # This creates a dh file with 4096 bits.

openvpn:
  server:
    srvr:
      server: '10.18.0.0 255.255.255.0'
      port: 8443
      status: /run/openvpn/openvpn-status.log
      crl: /etc/openvpn/crl.pem
  client:
    client:
      remote:
        - {{ credentials.domain }} 8443
