check_functionality_tux:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://tux/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755
