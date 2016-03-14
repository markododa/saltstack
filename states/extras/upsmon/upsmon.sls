install_samba:
  pkg.installed:
    - pkgs:
      - nut

      # COMMANDS
         
      # sudo upsdrvctl start
      # sudo service nut-server status
      # upsc openstackups
      # upscmd l openstackups
      
# To find out if your driver supports any extra settings, start it with
# the -h option and/or read the driver's documentation.

# LISTEN 127.0.0.1 3493 (default)
# admin:adminpass
# upsmon:pass

{% set myip = salt['grains.get']('ipv4')[0] %}

# needs to find the interface where other upsmonitors are

{% if myip == '127.0.0.1' %}    
{% set myip = salt['grains.get']('ipv4')[1] %}
{% endif %}    

{% if myip == '127.0.0.1' %}    
{% set myip = salt['grains.get']('ipv4')[2] %}
{% endif %}    

/etc/nut/ups.conf:
  file.managed:
    - source: salt://extras/upsmon/ups.conf
    - user: nut
    - group: nut
    - mode: 640
#    - mode: 644

/etc/nut/nut.conf:
  file.managed:
    - source: salt://extras/upsmon/nut.conf
    - user: nut
    - group: nut
    - mode: 640
#    - mode: 644
    
/etc/nut/upsd.users:
  file.managed:
    - source: salt://extras/upsmon/upsd.users
    - user: nut
    - group: nut
    - mode: 640 
    
/etc/nut/upsd.conf:
  file.managed:
    - source: salt://extras/upsmon/upsd.conf
    - user: nut
    - group: nut
    - mode: 640

/etc/nut/upsmon.conf:
  file.managed:
    - source: salt://extras/upsmon/upsmon.conf
    - user: nut
    - group: nut
    - mode: 640
    



    
# {% if domain != None %}

# reloadsmbconf:
  # cmd.run:
    # - name: smbcontrol all reload-config
    # - onlyif: test -e /etc/samba/smb.conf
        
# join_domain:
  # cmd.run:
    # - name: net ads join -U Administrator%{{ admin_password }} && touch /vapour/.fileshare-set && shutdown -r +1 "<< Reboot needed after joining domain >>" &
    # - onlyif: test ! -e /vapour/.fileshare-set

# {% endif %}

    
#reloadsmbd:
#  cmd.run:
#    - name: service smbd restart
#    - onlyif: test -e /etc/samba/smb.conf      
    
#reloadnmbd:
#  cmd.run:
#    - name: service nmbd restart
#    - onlyif: test -e /etc/samba/smb.conf    
    
