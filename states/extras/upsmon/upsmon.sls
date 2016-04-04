install_samba:
  pkg.installed:
    - pkgs:
      - nut

      # COMMANDS
         
      # sudo upsdrvctl start
      # sudo service nut-server status
      # upsc UPSserver
      # upscmd -l UPSserver
      # needs reboot or sudo upsdrvctl -u root start ?
      # upsmon -c fsd (simulate power failure)
     # sudo upsmon -c stop 
      
      
      # For best results, you should create a new normal user like "nutmon",
# and make it a member of a "nut" group or similar.  Then specify it
# here and grant read access to the upsmon.conf for that group.
#
# This user should not have write access to upsmon.conf.
      
      
# To find out if your driver supports any extra settings, start it with
# the -h option and/or read the driver's documentation.

# LISTEN 127.0.0.1 3493 (default)
# admin:adminpass
# upsmon:pass

# {% set myip = salt['grains.get']('ipv4')[0] %}

# needs to find the interface where other upsmonitors are

# {% if myip == '127.0.0.1' %}    
# {% set myip = salt['grains.get']('ipv4')[1] %}
# {% endif %}    

# {% if myip == '127.0.0.1' %}    
# {% set myip = salt['grains.get']('ipv4')[2] %}
# {% endif %}    

/etc/nut/ups.conf:
  file.managed:
    - source: salt://extras/upsmon/ups.conf
    - user: root
    - group: nut
    - mode: 640
#    - mode: 644

/etc/nut/nut.conf:
  file.managed:
    - source: salt://extras/upsmon/nut.conf
    - user: root
    - group: nut
    - mode: 640
#    - mode: 644
    
/etc/nut/upsd.users:
  file.managed:
    - source: salt://extras/upsmon/upsd.users
    - user: root
    - group: nut
    - mode: 640 
    
/etc/nut/upsd.conf:
  file.managed:
    - source: salt://extras/upsmon/upsd.conf
    - user: root
    - group: nut
    - mode: 640

/etc/nut/upsmon.conf:
  file.managed:
    - source: salt://extras/upsmon/upsmon.conf
    - user: root
    - group: nut
    - mode: 640
    


#probalby will need a reboot to apply new user permissins for usb/serail ports