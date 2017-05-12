include:
  - libvirt.lvm

gnutls-bin:
  pkg.installed: []

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
  service.running:
    - name: libvirtd
    - require:
      - pkg: libvirt-bin
      - network: br0
    - watch:
      - file: libvirt-bin

python-libvirt:
  pkg.installed: []

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

libvirt_keys:
  virt.keys
