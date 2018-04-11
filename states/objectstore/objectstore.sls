
/opt/minio:
  file.directory:
    - makedirs: True

/opt/minio/data
  file.directory:
    - makedirs: True

/usr/local/bin/minio:
  file.managed:
    - name: /opt/minio/minio
    - source: https://dl.minio.io/server/minio/release/linux-amd64/minio
    - source_hash: https://dl.minio.io/server/minio/release/linux-amd64/minio.sha256sum
    - user: root
    - group: root
    - mode: 655


install_test:
  cmd.run:
    - name: dpkg --force-all -i /opt/minio/minio.deb


check_functionality_objectstore:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://objectstore/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

