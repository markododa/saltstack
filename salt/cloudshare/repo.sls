{% from "cloudshare/map.jinja" import nextcloud with context %}

{% if grains['os_family'] == 'Debian' %}
nextcloud-repo:
  pkgrepo.managed:
    - name: {{ nextcloud.pkg_repo }}
    - file: {{ nextcloud.repo_file }}
    - key_url: {{ nextcloud.key_url }}
    - gpgcheck: 1
    - require_in:
      - pkg: {{ nextcloud.pkg }}
{%- endif %}

