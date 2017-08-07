install_proxy:
  pkg.installed:
    - pkgs:
      - squid3
      - lighttpd

#      - libtommath0
#      - libtommath1

#    - e2guardian
# squid da ne slusha osven za 127.0.0.1
# CNAME record na DNS za host: wpad kon web server sto ke gi sodrzi wpad.dat i proxy.pac 
# http://contentfilter.futuragts.com/wiki/doku.php?id=automatic_proxy_configuration    
# treba samo da slusha na 8080 i eventualno 80 (squid portata 3128 mora da e nedostapna)

{% set domain = salt['pillar.get']('domain') %}
{% set host_name = grains['id'] %}

/root/e2guardian.deb:
  file.managed:
    - source: salt://proxy/files/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb
    - user: root
    - group: root
    - mode: 755


stop_squid:
  service.dead:
    - name: squid

stop_lighttpd:
  service.dead:
    - name: lighttpd

cert_lhttps:
  cmd.run:
    - name: openssl req -new -x509 -keyout lighttpd.pem -out lighttpd.pem -days 3650 -nodes -sha256 -subj '/CN=mydomain.com/O=Web Proxy Certificate./C=US'

  
squid_use_hdd_as_cache_too:
 file.replace:
    - name: /etc/squid/squid.conf
    - pattern: http_port 3128
    - repl: http_port 127.0.0.1:3128

enable_hdd_cache:
  file.uncomment:
    - name: /etc/squid/squid.conf
    - char: '#'
    - regex: "cache_dir ufs /var.*"

prevent_localhost_url:
  file.uncomment:
    - name: /etc/squid/squid.conf
    - char: '#'
    - regex: "http_access deny to_localhost.*"

    # AUTO DISCOVERY, TREBA REALNO NA DRUG WEB SERVER DA SE, SERVER SO HOSTNAME WPAD,

/etc/lighttpd/lighttpd.conf:
  file.managed:
    - source: salt://proxy/files/lighttpd.conf
    - user: root
    - group: root
    - mode: 644

#/var/www/html/blocked.html:
#  file.managed:
#    - source: salt://proxy/files/blocked.html
#    - user: root
#    - group: root
#    - mode: 644

/var/www/html/wpad.dat:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 

#wpad_domain:
#  file.replace:
#    - name: /var/www/html/wpad.dat
#   - pattern: PROXY_DOMAIN
#   - repl: {{ domain }}

#wpad_host:
#  file.replace:
#    - name: /var/www/html/wpad.dat
#    - pattern: PROXY_HOST
#    - repl: {{ host_name }}
    
/var/www/html/proxy.pac:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 

#proxy_domain:
#  file.replace:
#   - name: /var/www/html/proxy.pac
#  - pattern: PROXY_DOMAIN
# - repl: {{ domain }}       
#
#proxy_host:
#  file.replace:
#    - name: /var/www/html/proxy.pac
#    - pattern: PROXY_HOST
#    - repl: {{ host_name }}

#remove_default_index:
#  cmd.run:
#    - name: rm /var/www/html/index.lighttpd.html

#show blocked info by default
/var/www/html/index.html:
  file.managed:
    - source: salt://proxy/files/index.html
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 


#show make different config page
/var/www/html/config.html:
  file.managed:
    - source: salt://proxy/files/config.html
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 

#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True

check_functionality_directory:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://directory/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

# E2GUARDIAN
install_e2b:
  cmd.run:
    - name: dpkg --force -i /root/e2guardian.deb

fix_e2b:
  cmd.run:
    - name: apt-get install -f -y

stop_e2guardian:
  service.dead:
    - name: e2guardian

/etc/e2guardian/updateBL.sh:
  file.managed:
    - source: salt://proxy/files/updateBL.sh
    - user: root
    - group: root
    - mode: 754

/etc/e2guardian/e2guardian.conf:
  file.managed:
    - source: salt://proxy/files/e2guardian.conf
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/e2guardianf1.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf1.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 

/etc/e2guardian/e2guardianf2.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf2.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 


/etc/e2guardian/e2guardianf3.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf3.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - context:
      PROXY_DOMAIN: {{ domain }}
      PROXY_HOSTNAME: {{ host_name }} 


/etc/e2guardian/lists/bannedsitelist1:
  file.managed:
    - source: salt://proxy/files/bannedsitelist1
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/bannedsitelist2:
  file.managed:
    - source: salt://proxy/files/bannedsitelist2
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/bannedsitelist3:
  file.managed:
    - source: salt://proxy/files/bannedsitelist3
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/exceptionsitelist1:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist1
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/exceptionsitelist2:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist2
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/exceptionsitelist3:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist3
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/exceptionextensionlist:
  file.managed:
    - source: salt://proxy/files/exceptionextensionlist
    - user: root
    - group: root
    - mode: 644

/etc/e2guardian/lists/authplugins/ipgroups:
  file.managed:
    - source: salt://proxy/files/ipgroups
    - user: root
    - group: root
    - mode: 644

/usr/share/e2guardian/languages/ukenglish/template.html:
  file.managed:
    - source: salt://proxy/files/template.html
    - user: root
    - group: root
    - mode: 644

#get_blacklists:
# cmd.run:
#    - name: /etc/e2guardian/updateBL.sh
  
squid:
  service.running:
    - enable: True

e2guardian:
  service.running:
    - enable: True

lighttpd:
  service.running:
    - enable: True

# start_squid:
  # cmd.run:
    # - name: service squid start    

# start_e2g:
  # cmd.run:
    # - name: service e2guardian start   
