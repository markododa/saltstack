{% from "backuppc/map.jinja" import backup4 with context %}

{% set os = salt['grains.get']('os', None) %}
{% set os_family = salt['grains.get']('os_family', None) %}
{% set backup4_password = salt['pillar.get']('admin_password') %}

install-pkgs:
  pkg.installed:
    - pkgs:
      - smbclient
      - netcat
      - sshpass
      - apache2
      - apache2-utils
      - libapache2-mod-perl2
      - libjson-perl
      - glusterfs-client
      - par2 perl
      - smbclient
      - rsync
      - tar
      - sendmail
      - gcc
      - zlib1g
      - zlib1g-dev
      - libapache2-mod-scgi
      - rrdtool
      - git
      - make
      - wget
      - perl-doc
      - libfile-listing-perl
      - libxml-rss-perl
      - libcgi-session-perl
    - require_in:
      - file: /etc/samba/smb.conf

/etc/samba/smb.conf:
  file.replace:
    - pattern: "workgroup = .*"
    - repl: 'workgroup = {% filter upper %}{{salt['pillar.get']('shortdomain')}}{% endfilter %}'


/root/installbackuppc4.sh:
  file.managed:
    - source:
      - salt://backup4/files/installbackuppc4.sh
    - user: root
    - group: root
    - mode: 755


replace_pass:
  file.replace:
    - name: /root/installbackuppc4.sh
    - pattern: "PASSWORD=.*"
    - repl: 'PASSWORD="{{ backup4_password }}"'

run_installer:
  cmd.run:
    - name: /root/installbackuppc4.sh

# force_smb2:
#   file.line:
#     - name: /etc/samba/smb.conf
#     - mode: ensure
#     - content: client max protocol = SMB2
#     - after: \[global\]


# backup4:
#   pkg.installed:
#     - name: {{ backup4.server.pkg }}

# {% if backup4_password %}
# backup4_htpasswd:
#   webutil.user_exists:
#     - name: {{ backup4.server.webuser }}
#     - htpasswd_file: {{ backup4.server.configdir }}/htpasswd
#     - password: {{ backup4_password }}
#     - force: true
#     - require:
#       - pkg: backuppc
# {% endif %}

backup4_config:
  file.managed:
    - name: {{ backup4c.server.configdir }}/config.pl
    - template: jinja
    - source: salt://backup4/files/config.pl
    - user: {{ backup4.server.user }}
    - group: {{ backup4.server.group }}


# {% set multisite = salt['pillar.get']('multisite') %}

# {% if multisite != True %}

# 'rm /etc/apache2/sites-enabled/000-default.conf':
#   cmd.run:
#     - onlyif: test -e /etc/apache2/sites-enabled/000-default.conf

# remove_alias:
#   file.replace:
#     - name: /etc/apache2/conf-available/backuppc.conf
#     - pattern: Alias /backuppc /usr/share/backuppc/cgi-bin/
#     - repl: |
#         Alias /backuppc/image /usr/share/backuppc/image
#         DocumentRoot /usr/share/backuppc/cgi-bin/
# apache2:
#   service.running:
#     - watch:
#       - file: /etc/apache2/conf-available/backuppc.conf
# {% endif %}



# create_key:
#   cmd.run:
#     - name: su -s /bin/bash -c "ssh-keygen -q -f /var/lib/backuppc/.ssh/id_rsa -N ''" -l backuppc
#     - require:
#       - pkg: backuppc
#     - onlyif: test ! -e /var/lib/backuppc/.ssh/id_rsa

push-key:
  cmd.run:
    - name: salt-call event.send  backuppc/pubkey pubkey="`cat /var/lib/backuppc/.ssh/id_rsa.pub`"
    - onlyif: test -e /var/lib/backuppc/.ssh/id_rsa

/usr/local/backuppc/lib/BackupPC/CGI/JSON.pm:
  file.managed:
    - source: salt://backup4/files/JSON.pm

#Not sure about this
/usr/local/backuppc/lib/realindex.cgi:
  file.blockreplace:
    - marker_start: '"rss"                        => "RSS",'
    - marker_end: ');'
    - content: '    "json"                       => "JSON",'

/dev/vdb:
  blockdev.formatted:
    - onlyif:
        - test -e /dev/vdb


/mnt/va-backup:
  mount.mounted:
    - device: /dev/vdb
    - fstype: ext4
    - mkmnt: True
    - opts: defaults,noatime
    - onlyif:
        - test -e /dev/vdb

'mv /var/lib/backuppc /mnt/va-backup/':
  cmd.run:
    - onlyif:
      - test -e /mnt/va-backup/
      - test ! -e /mnt/va-backup/backuppc
      - mount | grep -q /mnt/va-backup

'ln -sfn /mnt/va-backup/backuppc /var/lib/backuppc':
  cmd.run:
    - onlyif:
        - test -e /mnt/va-backup/backuppc
        - mount | grep -q /mnt/va-backup


#### functionality script
/usr/lib/nagios/plugins/check_functionality.sh:
  file.managed:
    - source:
      - salt://backuppc/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

/usr/bin/backuppc_servermsg:
  file.managed:
    - source:
      - salt://backuppc/files/backuppc_servermsg
      - user: root
      - group: root
      - mode: 0755

#should not overwrite just check in archive line is there
/etc/BackupPC/hosts:
  file.managed:
    - source:
      - salt://backup4/files/hosts
      - user: backuppc
      - group: backuppc
      - mode: 0640


/etc/BackupPC/pc/archive.pl:
  file.managed:
    - source:
      - salt://backup4/files/archive.pl
      - user: backuppc
      - group: backuppc
      - mode: 0640


#Should be only once
#/etc/BackupPC/archive.pl:
#  file.append:
#    - text: "$Conf{XferMethod} = 'archive';"

#not necessary?
chmod +x /usr/bin/backuppc_servermsg:
  cmd.run

/etc/sudoers.d/nagios:
  file.append:
    - text: "nagios ALL = (backuppc) NOPASSWD: /usr/local/backuppc/bin/BackupPC_serverMesg"

backup4-restart:
  service.running:
    - name: backuppc
    - watch:
      - event: salt/app/new

salt/app/new:
  event.send:
    - data:
        sls: base.backup
