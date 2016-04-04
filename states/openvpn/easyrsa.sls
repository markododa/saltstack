install_easyrsa:
  archive.extracted:
    - name: /etc/openvpn/easyrsa
    - source: salt://openvpn/files/easyrsa.tgz
    - archive_format: tar

setup_rsa:
  cmd.run:
    - name: |
        ./easyrsa init-pki
        echo openvp-server | ./easyrsa build-ca nopass
        ./easyrsa build-server-full server nopass
    - cwd: /etc/openvpn/easyrsa
    - unless: test -e /etc/openvpn/easyrsa/pki/private/server.key

create_crl:
  cmd.run:
    - name: |
        ./easyrsa gen-crl
        cp /etc/openvpn/easyrsa/pki/crl.pem /etc/openvpn/
        chown nobody:nogroup /etc/openvpn/crl.pem
    - cwd: /etc/openvpn/easyrsa
    - unless: test -e /etc/openvpn/easyrsa/pki/crl.pem
