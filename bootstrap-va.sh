#!/bin/bash
#export SALTTREE=salt-tree.tar.gz
wget -O - https://repo.saltstack.com/apt/debian/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/latest jessie main' > /etc/apt/sources.list.d/salt.list
apt-get update -y
apt-get install --no-install-recommends salt-master -y
#tar xzfv $SALTTREE -C /srv
cd "$(dirname "$0")"
mkdir /srv/{salt,pillar,reactor,salt/_modules}
cp -R states/* /srv/salt
cp -R pillars/* /srv/pillar
cp -R reactor/* /srv/reactor
cp -R modules/* /srv/salt/_modules
#setup pillars
cp *.sls /srv/pillar
cp /srv/salt/salt-master/files/master /etc/salt/master 
service salt-master restart
apt-get install salt-minion -y
echo "master: localhost" >> /etc/salt/minion
echo "role: monitoring" > /etc/salt/grains
service salt-minion restart
sleep 30
salt-key -y -a `hostname`
salt-call --local state.highstate -l quiet
