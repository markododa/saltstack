nova-compute:
  pkg.installed

add_compute_configs:
  file.blockreplace:
    - name: /etc/nova/nova.conf
    - marker_start: '[vnc]'
    - marker_end: 'vncserver_listen = 127.0.0.1'
    - content: |
        enabled = True
        novncproxy_base_url = http://{{grains['host']}}:6080/vnc_auto.html

compute-restart:
  service.running:
    - restart: True
    - name: nova-compute
