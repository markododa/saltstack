install_gnutls:
  pkg.installed:
    - pkg: gnutls

libvirt-bin:
  pkg.installed: []
  file.managed:
    - name: /etc/default/libvirtd
    - contents: 'LIBVIRTD_ARGS="--listen"'
    - require:
      - pkg: libvirt-bin
  virt.keys:
    - require:
      - pkg: gnutls-bin
      - expiration_days: 3650
  service.running:
    - name: libvirtd
    - require:
      - pkg: libvirt-bin
      - network: br0
    - watch:
      - file: libvirt-bin

libguestfs:
  pkg.installed:
    - pkgs:
      - libguestfs-tools

eno1:
  network.managed:
    - enabled: True
    - type: eth
    - bridge: br0

br0:
  network.managed:
    - enabled: True
    - type: bridge
    - proto: dhcp
    - ports: eno1
    - require:
      - network: eno1
