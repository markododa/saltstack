install_proxy:
  pkg.installed:
    - pkgs:
      - squid3
      - lighttpd
      - libtommath0


# http://contentfilter.futuragts.com/wiki/doku.php?id=automatic_proxy_configuration    


{% set domain = salt['pillar.get']('domain') %}
{% set host_name = grains['id'] %}
{% set dcip = salt['mine.get'](tgt='role:directory',fun='inventory',tgt_type='grain')['va-directory']['ip4_interfaces']['eth0'][0] %}
{% set my_ip = salt['pillar.get']('proxy_ip') %}

# SET IP IN PILLARS TO FORCE DESIRED IP ADDRESS FOR PROXY SERVICE


{% if my_ip != None %}  


/root/e2guardian.deb:
  file.managed:
    - source: salt://proxy/files/e2guardian_3.4.0.3_wheezy-jessie_amd64.deb
    - user: root
    - group: root
    - mode: 755

stop_squid3:
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
    - regex: "cache_dir ufs /var.*"

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
      PROXY_IP: {{ my_ip }} 

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
      PROXY_IP: {{ my_ip }} 

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
      PROXY_IP: {{ my_ip }} 


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
      PROXY_IP: {{ my_ip }} 

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
    - replace: False
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }}  
      PROXY_IP: {{ my_ip }} 

/etc/e2guardian/e2guardianf2.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf2.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - replace: False
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }}  
      PROXY_IP: {{ my_ip }} 


/etc/e2guardian/e2guardianf3.conf:
  file.managed:
    - source: salt://proxy/files/e2guardianf3.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
    - replace: False
    - context:
      PROXY_DOMAIN: {% filter lower %}{{ domain }}{% endfilter %}
      PROXY_HOSTNAME: {{ host_name }}  
      PROXY_IP: {{ my_ip }} 


/etc/e2guardian/lists/bannedsitelist1:
  file.managed:
    - source: salt://proxy/files/bannedsitelist1
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/bannedsitelist2:
  file.managed:
    - source: salt://proxy/files/bannedsitelist2
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/bannedsitelist3:
  file.managed:
    - source: salt://proxy/files/bannedsitelist3
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/exceptionsitelist1:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist1
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/exceptionsitelist2:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist2
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/exceptionsitelist3:
  file.managed:
    - source: salt://proxy/files/exceptionsitelist3
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/exceptionextensionlist:
  file.managed:
    - source: salt://proxy/files/exceptionextensionlist
    - user: root
    - group: root
    - mode: 644
    - replace: False

/etc/e2guardian/lists/authplugins/ipgroups:
  file.managed:
    - source: salt://proxy/files/ipgroups
    - user: root
    - group: root
    - mode: 644
    - replace: False

/usr/share/e2guardian/languages/ukenglish/template.html:
  file.managed:
    - source: salt://proxy/files/template.html
    - user: root
    - group: root
    - mode: 644

make_blacklists:
  cmd.run:
    - name: /etc/e2guardian/make_empty_bl.sh

/etc/e2guardian/lists/blacklists/_custom/domains:
  file.append:
    - text: '#listcategory: "Custom List"'


label_categories:
  file.managed:
    - name: /etc/e2guardian/label_categories.sh
    - source: salt://proxy/files/label_categories.sh
    - user: root
    - group: root
    - mode: 755

label_categories_run:
  cmd.run:
    - name: /etc/e2guardian/label_categories.sh

#get_blacklists:
# cmd.run:
#    - name: /etc/e2guardian/updateBL.sh

writableresolve_proxy:
  cmd.run:
    - name: chattr -i /etc/resolv.conf 

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

squid3:
  service.running:
    - enable: True

e2guardian:
  service.running:
    - enable: True

lighttpd:
  service.running:
    - enable: True


{% endif %}


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


restart_functionality_proxy:
  file.managed:
    - name: /usr/lib/nagios/plugins/restart_functionality.sh
    - source: salt://proxy/files/restart_functionality.sh
    - user: root
    - group: root
    - mode: 755

top_visits:
  file.managed:
    - name: /etc/e2guardian/top_visits.sh
    - source: salt://proxy/files/top_visits.sh
    - user: root
    - group: root
    - mode: 755

top_blocked:
  file.managed:
    - name: /etc/e2guardian/top_blocked.sh
    - source: salt://proxy/files/top_blocked.sh
    - user: root
    - group: root
    - mode: 755
    
last_blocked:
  file.managed:
    - name: /etc/e2guardian/last_blocked.sh
    - source: salt://proxy/files/last_blocked.sh
    - user: root
    - group: root
    - mode: 755

