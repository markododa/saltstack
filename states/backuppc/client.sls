{% from "backuppc/map.jinja" import backuppc with context %}

backuppc-client:
  pkg.installed:
    - pkgs: {{ backuppc.client.pkgs }}

