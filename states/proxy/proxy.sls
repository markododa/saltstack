install_proxy:
  pkg.installed:
    - pkgs:
      - squid3
      - lighttpd
      - libtommath0

# CNAME record na DNS za host: wpad kon web server sto ke gi sodrzi wpad.dat i proxy.pac 
# http://contentfilter.futuragts.com/wiki/doku.php?id=automatic_proxy_configuration    
# treba samo da slusha na 8080 i eventualno 80 (squid portata 3128 mora da e nedostapna)

{% set domain = salt['pillar.get']('domain') %}
{% set host_name = grains['id'] %}
{% set dcip = salt['mine.get'](tgt='role:directory',fun='inventory',expr_form='grain')['va-directory']['ip4_interfaces']['eth0'][0] %}

/root/e2guardian.deb:
  file.managed:
    - source: salt://proxy/files/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb
    - user: root
    - group: root
    - mode: 755

stop_squid:
  service.dead:
    - name: squid3

stop_lighttpd:
  service.dead:
    - name: lighttpd

/etc/lighttpd/certs/:
  file.directory:
    - makedirs: True

cert_lhttps:
  cmd.run:
    - name: openssl req -new -x509 -keyout /etc/lighttpd/certs/lighttpd.pem -out /etc/lighttpd/certs/lighttpd.pem -days 3650 -nodes -sha256 -subj '/CN={{ host_name }}.{% filter lower %}{{ domain }}{% endfilter %}/O=VA-Proxy/C=US'
  
squid_2_e2g_only:
 file.replace:
    - name: /etc/squid3/squid.conf
    - pattern: http_port 3128
    - repl: http_port 127.0.0.1:3128

enable_hdd_cache:
  file.uncomment:
    - name: /etc/squid3/squid.conf
    - char: '#'
    # - regex: "cache_dir ufs /var.*"
    - regex: "cache_dir ufs /var/spool/squid3 100 16 256"

prevent_localhost_url:
  file.uncomment:
    - name: /etc/squid3/squid.conf
    - char: '#'
    - regex: "http_access deny to_localhost.*"

/etc/lighttpd/lighttpd.conf:
  file.managed:
    - source: salt://proxy/files/lighttpd.conf
    - user: root
    - group: root
    - mode: 644

# auto discovery, todo: register this hostname in dns server. also add record for host 'wpad'

/var/www/html/wpad.dat:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }} 

/var/www/html/proxy.pac:
  file.managed:
    - source: salt://proxy/files/wpad
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }} 

#show blocked info by default
/var/www/html/index.html:
  file.managed:
    - source: salt://proxy/files/index.html
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
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
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }} 

# E2GUARDIAN
install_e2b:
  cmd.run:
    - name: dpkg --force-all -i /root/e2guardian.deb

fix_e2b:
  cmd.run:
    - name: apt-get install -f -y

stop_e2guardian:
  service.dead:
    - name: e2guardian

/etc/e2guardian/make_empty_bl.sh:
  file.managed:
    - source: salt://proxy/files/make_empty_bl.sh
    - user: root
    - group: root
    - mode: 754

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
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }} 

/etc/e2guardian/e2guardianf2.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf2.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }} 


/etc/e2guardian/e2guardianf3.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf3.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
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

make_blacklists:
  cmd.run:
    - name: /etc/e2guardian/make_empty_bl.sh

#get_blacklists:
# cmd.run:
#    - name: /etc/e2guardian/updateBL.sh


/etc/resolv.conf:
  file.managed:
    - source: salt://proxy/files/resolv.conf
    - user: root
    - group: root
    - mode: 777

resolv_proxy:
  file.replace:
    - name: /etc/resolv.conf
    - pattern: DOMAIN
    - repl: {{ domain }}

resolvednsip_proxy:
  file.replace:
    - name: /etc/resolv.conf
    - pattern: DCIP
    - repl: {{ dcip }}
    
readableresolve_proxy:
  cmd.run:
    - name: chattr +i /etc/resolv.conf 
 
squid:
  service.running:
    - enable: True

e2guardian:
  service.running:
    - enable: True

lighttpd:
  service.running:
    - enable: True

#### functionality script
/usr/lib/nagios/plugins/:
  file.directory:
    - makedirs: True

check_functionality_proxy:
  file.managed:
    - name: /usr/lib/nagios/plugins/check_functionality.sh
    - source: salt://proxy/files/check_functionality.sh
    - user: root
    - group: root
    - mode: 755

