install_gnutls:
  pkg.installed:
    - name: gnutls-bin

{% set interface = salt['pillar.get']('bridge_interface','eth0') %}
{% if grains['oscodename'] == "stretch" %}
{% set libvirt_pkgs = ['libvirt-daemon-system', 'libvirt-clients'] %}
{% else %}
{% set libvirt_pkgs = ['libvirt-bin'] %}
{% endif%}

{% for pkg in libvirt_pkgs %}
{{pkg}}:
  pkg.installed: []
{% endfor %}

libvirtd:
  file.managed:
    - name: /etc/default/libvirtd
    - contents: 'libvirtd_opts="--listen"'
  virt.keys:
    - require:
      - pkg: gnutls-bin
    - expiration_days: 3650
  service.running:
    - name: libvirtd
    - require:
      - network: br0
    - watch:
      - file: /etc/default/libvirtd

libguestfs:
  pkg.installed:
    - pkgs:
      - libguestfs-tools

{{interface}}:
  network.managed:
    - enabled: True
    - type: eth
    - bridge: br0

br0:
  network.managed:
    - enabled: True
    - type: bridge
    - proto: dhcp
    - ports: {{interface}}
    - require:
      - network: {{interface}}

virsh net-autostart default:
  cmd.run:
    - onlyif: virsh net-info default|grep -q "Autostart.*no"

virsh net-start default:
  cmd.run:
    - onlyif: virsh net-info default|grep -q "Active.*no"
