lvm2:
  pkg.installed

{{pillar['cinder_pv']}}:
  lvm.pv_present

cinder_volumes:
  lvm.vg_present:
    - devices: {{pillar['cinder_pv']}}
