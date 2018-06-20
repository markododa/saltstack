get_mattermost:
  archive.extracted:
    - name: /opt/
    - source: https://releases.mattermost.com/3.2.0/mattermost-team-3.2.0-linux-amd64.tar.gz
    - archive_format: tar
    - if_missing: /opt/mattermost
    - source_hash: md5=4cdc51e5793b44e9e69919d747a7f947
