user:
  postgres_user.present:
    - name: "mattermost"
    - password: "{{ salt['grains.get_or_set_hash']('mattermost_db_pass') }}"
#    - password: test
    - createdb: True
    - login: True
postgresql:
  pkg:
    - name: postgresql
    - installed

create_db:
  postgres_database.present:
    - name: "mattermost"
    - db_user: "mattermost"
    - db_password: "{{ salt['grains.get_or_set_hash']('mattermost_db_pass') }}"
    - db_host: 127.0.0.1
#    - db_password: test
