plugins

/usr/share/redmine
bundle exec rake redmine:plugins:migrate RAILS_ENV=production

/usr/share/redmine$ sudo bundle exec rake redmine:plugins:migrate RAILS_ENV=production

git clone https://github.com/gyselroth/redmine-plugin-autorespond.git


-------
git clone git://github.com/thorin/redmine_ldap_sync.git
upgrade - Backup and replace the old plugin directory with the new plugin files. If you are downloading the plugin directly from GitHub, you can do so by changing into the plugin directory and issuing the command git pull.

Update the ruby gems by changing into the redmine's directory and run the following command.

bundle install
upgrade - Still on the redmine's directory, run the following command to upgrade your database (make a db backup before).

rake redmine:plugins:migrate RAILS_ENV=production
Change into redmines directory {RAILS_ROOT} and run the following command.

rake -T redmine:plugins:ldap_sync RAILS_ENV=production
-------



https://framagit.org/infopiiaf/redhopper.git

stall the missing gems with bundle install (within redmine's root folder and not redhopper's one)
Run the migrations of the plugin: RAILS_ENV=production bundle exec rake redmine:plugins:migrate NAME=redhopper

-------------




restart redmine

touch /usr/share/redmine/tmp/restart.txt




THE BEST:
http://www.redmine.org/projects/redmine/wiki/HowTo_Install_Redmine_on_Ubuntu_step_by_step


apt-get install apache2 libapache2-mod-passenger -y

apt-get install -y -q mysql-server mysql-client 


mysql -u root




redmine-db1:
  cmd.run:
    - name: echo "CREATE DATABASE redmine character SET utf8; CREATE user 'redmine'@'localhost' IDENTIFIED BY 'redmine'; GRANT ALL privileges ON redmine.* TO 'redmine'@'localhost'; set password for 'redmine'@'localhost'= password('{{ dbpass }}');flush privileges;" | mysql -uroot
    - unless: echo 'show databases;' | mysql -uroot | grep -q redmine





mkdir -p /usr/share/redmine/templates/
mkdir -p /etc/dbconfig-common/redmine/instances/

/usr/share/redmine/templates/database-mysql2.yml.template


/etc/dbconfig-common/redmine/instances/default.conf



apt-get install redmine redmine-mysql  -y -q



gem update  --no-ri --no-rdoc
#gem install bundler

gem install bundler --no-ri --no-rdoc


/etc/apache2/mods-available/passenger.conf



ln -s /usr/share/redmine/public /var/www/html/redmine

root@debian:/var/www/html# cat /etc/apache2/sites-available/000-default.conf


touch /usr/share/redmine/Gemfile.lock

/usr/share/redmine/Gemfile.lock:
  file.touch
chown www-data:www-data /usr/share/redmine/Gemfile.lock

service apache2 restart


---------------






PASS=`sudo awk '/password/ { print $3;exit }' /etc/mysql/debian.cnf`
echo "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MyNewPass');" \
| mysql -u debian-sys-maint -p$PASS



TRY
https://www.howtoforge.com/tutorial/how-to-install-redmine-with-nginx-on-ubuntu/

apt-get install nginx libssl-dev mysql-server libmysqlclient-dev git-core subversion imagemagick libmagickwand-dev ruby ruby-dev libcurl4-openssl-dev 

gpg --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable

source /usr/local/rvm/scripts/rvm
echo '[[ -s "/usr/local/rvm/scripts/rvm" ]] && source "/usr/local/rvm/scripts/rvm"' >> ~/.bashrc

git clone git://github.com/jnstq/rails-nginx-passenger-ubuntu.git
mv rails-nginx-passenger-ubuntu/nginx/nginx /etc/init.d/nginx
chown root:root /etc/init.d/nginx
mkdir -p /opt/nginx/conf/
nano /opt/nginx/conf/nginx.conf

====================
#user  nobody;
#Defines which Linux system user will own and run the Nginx server

worker_processes  1;
#Referes to single threaded process. Generally set to be equal to the number of CPUs or cores.

#error_log  logs/error.log; #error_log  logs/error.log  notice;
#Specifies the file where server logs. 

#pid        logs/nginx.pid;
#nginx will write its master process ID(PID).

events {
    worker_connections  1024;
    # worker_processes and worker_connections allows you to calculate maxclients value: 
    # max_clients = worker_processes * worker_connections
}


http {
    include       mime.types;
    # anything written in /opt/nginx/conf/mime.types is interpreted as if written inside the http { } block

    default_type  application/octet-stream;
    #

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    # If serving locally stored static files, sendfile is essential to speed up the server,
    # But if using as reverse proxy one can deactivate it
    
    #tcp_nopush     on;
    # works opposite to tcp_nodelay. Instead of optimizing delays, it optimizes the amount of data sent at once.

    #keepalive_timeout  0;
    keepalive_timeout  65;
    # timeout during which a keep-alive client connection will stay open.

    #gzip  on;
    # tells the server to use on-the-fly gzip compression.

    server {

        #  server_name redmine.va.mk # redmine.com;
          root /opt/redmine/public;
          passenger_enabled on;
          client_max_body_size      10m; # Max attachemnt size

        # You would want to make a separate file with its own server block for each virtual domain
        # on your server and then include them.
        listen       80;
        #tells Nginx the hostname and the TCP port where it should listen for HTTP connections.
        # listen 80; is equivalent to listen *:80;
        
        server_name  localhost;
        # lets you doname-based virtual hosting

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        # location / {
          #  The location setting lets you configure how nginx responds to requests for resources within the server.
            # root   html;
            # index  index.html index.htm;
        # }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        # error_page   500 502 503 504  /50x.html;
        # location = /50x.html {
            # root   html;
        # }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
=================

update-rc.d nginx defaults

cd /opt
 svn co http://svn.redmine.org/redmine/branches/3.4-stable redmine
 cd /opt/redmine


nano config/database.yml
Add following lines

production:
  adapter: mysql2
  database: redmine
  host: localhost
  username: redmine
  password: redmine
  encoding: utf8

development:
  adapter: mysql2
  database: redmine 
  host: localhost
  username: redmine
  password: redmine
  encoding: utf8


gem install bundler --no-ri --no-rdoc
bundle install


cd /opt/redmine
chown -R www-data:www-data files log tmp public/plugin_assets config.ru
chmod -R 755 files log tmp public/plugin_assets


mysql -u root -p
Execute following lines to MySQL

CREATE DATABASE redmine character SET utf8;
CREATE user 'redmine'@'localhost' IDENTIFIED BY 'redmine';
GRANT ALL privileges ON redmine.* TO 'redmine'@'localhost';
exit



bundle exec rake db:migrate
bundle exec rake redmine:plugins


bundle exec rake generate_secret_token 



service nginx start

touch /opt/redmine/tmp/restart.txt