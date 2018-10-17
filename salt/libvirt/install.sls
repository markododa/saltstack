install_gnutls:
  pkg.installed:
    - name: gnutls-bin

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
    - contents: 'LIBVIRTD_ARGS="--listen"'
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
