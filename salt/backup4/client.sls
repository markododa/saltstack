{% from "backup4/map.jinja" import backup4 with context %}

backuppc-client:
  pkg.installed:
    - pkgs: {{ backuppc.client.pkgs }}

