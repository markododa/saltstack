{% if salt['pillar.get']('create_vg') == True %}
{% set disks = salt['pillar.get']('disks') %}
{% for disk in disks %}
parted {{disk}} mkpart primary ext2 0% 100%:
  cmd.run:
   - onlyif: test ! -e {{disk}}1
{% endfor %}

/dev/md126:
  raid.present:
    - level: 5
    - devices:
    {%- for disk in disks %}
      - {{disk}}1
    {%- endfor %}
    - run: True

create_pv:
  lvm.pv_present:
    - name: /dev/md126

lvm-volumes:
  lvm.vg_present:
    - devices: /dev/md126

{% endif %}
