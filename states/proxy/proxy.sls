install_proxy:
  pkg.installed:
    - pkgs:
      - squid3
#    - e2guardian
     
# squid da ne slusha osven za 127.0.0.1
# CNAME record na DNS za host: wpad kon web server sto ke gi sodrzi wpad.dat i proxy.pac 
# http://contentfilter.futuragts.com/wiki/doku.php?id=automatic_proxy_configuration    
# treba samo da slusha na 8080 i eventualno 80 (squid portata 3128 mora da e nedostapna)

{% set domain = salt['pillar.get']('domain') %}

/root/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb:
  file.managed:
    - source: salt://proxy/files/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb
    - user: root
    - group: root
    - mode: 755
    
install_e2b:
  cmd.run:
    - name: dpkg -i /root/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb
    
fix_e2b:
  cmd.run:
    - name: apt-get install -f -y
# ima li alternativna komanda za ova gore?  
  
/etc/e2guardian/updateBL.sh:
  file.managed:
    - source: salt://proxy/files/updateBL.sh
    - user: root
    - group: root
    - mode: 755
    
/etc/e2guardian/e2guardian.conf:
  file.managed:
    - source: salt://proxy/files/e2guardian.conf
    - user: root
    - group: root
    - mode: 644
    
/etc/e2guardian/e2guardianf1.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf1.conf
    - user: root
    - group: root
    - mode: 644
    
/etc/e2guardian/e2guardianf2.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf2.conf
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/bannedsitelistSTD:
  file.managed:
    - source: salt://proxy/files/bannedsitelistSTD
    - user: root
    - group: root
    - mode: 755
    
/etc/e2guardian/lists/bannedsitelistVIP:
  file.managed:
    - source: salt://proxy/files/bannedsitelistVIP
    - user: root
    - group: root
    - mode: 755

/etc/e2guardian/lists/exceptionsitelistSTD:
  file.managed:
    - source: salt://proxy/files/exceptionsitelistSTD
    - user: root
    - group: root
    - mode: 755

/etc/e2guardian/lists/exceptionsitelistVIP:
  file.managed:
    - source: salt://proxy/files/exceptionsitelistVIP
    - user: root
    - group: root
    - mode: 755

/etc/e2guardian/lists/authplugins/ipgroups:
  file.managed:
    - source: salt://proxy/files/ipgroups
    - user: root
    - group: root
    - mode: 755

/usr/share/e2guardian/languages/ukenglish/template.html:
  file.managed:
    - source: salt://proxy/files/template.html
    - user: root
    - group: root
    - mode: 755
 
get_blacklists:
  cmd.run:
    - name: /etc/e2guardian/updateBL.sh
    
restart_e2g:
  cmd.run:
    - name: service e2guardian restart

# AUTO DISCOVERY, TREBA REALNO NA DRUG INTERENT WEB SERVER DA SE, SERVER SO HOSTNAME WPAD,

/var/www/html/wpad.dat:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 777

wpad:
  file.replace:
    - name: /var/www/html/wpad.dat
    - pattern: DOMAIN
    - repl: {{ domain }}

    
/var/www/html/proxy.pac:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 777
       
proxy:
  file.replace:
    - name: /var/www/html/proxy.pac
    - pattern: DOMAIN
    - repl: {{ domain }}

  
