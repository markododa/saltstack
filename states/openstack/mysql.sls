{% from "openstack/pass.jinja" import passwords with context %}
{% from "openstack/pass.jinja" import databases with context %}

{% for database in databases %}
{% set user = database %}
{% if database == 'nova_api' %}
{% set user = 'nova' %}
{% endif %}
{% set user_dbpass = [user,'_dbpass']| join() %}
{% set password = salt['grains.get'](user_dbpass) %}
{{database}}:
  cmd.run:
    - name: echo "CREATE DATABASE {{database}};" | mysql -uroot
    - unless: echo 'show databases;' | mysql -uroot |grep -q '{{database}}$'

echo "GRANT ALL PRIVILEGES ON {{database}}.* TO {{user}}@'localhost' IDENTIFIED BY '{{password}}';" | mysql -uroot:
  cmd.run

echo "GRANT ALL PRIVILEGES ON {{database}}.* TO {{user}}@'%' IDENTIFIED BY '{{password}}';" | mysql -uroot:
  cmd.run

{% endfor %}
