openjdk-8-jdk:
  pkg.installed

apt-transport-https:
  pkg.installed

repo_add:
  pkgrepo.managed:
    - humanname: cyconet jessie backports
    - name: deb https://artifacts.elastic.co/packages/6.x/apt stable main
    - file: /etc/apt/sources.list.d/elasticsearch.list
    - key_url: https://artifacts.elastic.co/GPG-KEY-elasticsearch
    - watch:
      - pkg: apt-transport-https

install_pkgs:
  pkg.installed:
    - pkgs:
      - elasticsearch
      - kibana
      - logstash
      - nginx
      - ssl-cert

elasticsearch:
  service.running:
    - restart: True
    - enable: True
    - watch:
      - pkg: elasticsearch

kibana:
  service.running:
    - enable: True
    - restart: True
    - watch:
      - pkg: kibana

echo "admin:$(openssl passwd -apr1 {{salt['pillar.get']('admin_password')}})" | sudo tee -a /etc/nginx/htpasswd.kibana:
  cmd.run:
    - unless: test -e /etc/nginx/htpasswd.kibana

rm /etc/nginx/sites-enabled/default:
  cmd.run
    - unless: test -e /etc/nginx/sites-enabled/default

/etc/nginx/sites-available/kibana:
  file.managed:
    - source: salt://elk/kibana.nginx

/etc/nginx/sites-enabled/kibana:
  file.symlink:
    - target: /etc/nginx/sites-available/kibana

nginx:
  service.running:
    - enable: True
    - restart: True
    - watch:
      - file: /etc/nginx/sites-available/kibana

logstash:
  service.running:
    - enable: True
    - restart: True
    - watch:
      - pkg: logstash
