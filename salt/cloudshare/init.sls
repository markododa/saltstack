apt-transport-https:
  pkg.installed:
    - order: first
include:
  - cloudshare.mysql
  - cloudshare.repo
  - cloudshare.setup
  - cloudshare.ldap
