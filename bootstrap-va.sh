#!/bin/bash
set -e
#export SALTTREE=salt-tree.tar.gz
wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main' > /etc/apt/sources.list.d/salt.list
apt-get update -y
apt-get install --no-install-recommends salt-master -y
#tar xzfv $SALTTREE -C /srv
cd "$(dirname "$0")"
mkdir /srv/{salt,pillar,reactor}
cp -R salt/* /srv/salt
cp -R pillar/* /srv/pillar
cp -R reactor/* /srv/reactor
#setup pillars
cp *.sls /srv/pillar
cp /srv/salt/salt-master/files/master /etc/salt/master 
service salt-master restart
apt-get install salt-minion -y
echo "master: localhost" >> /etc/salt/minion
echo "role: monitoring" > /etc/salt/grains
service salt-minion restart
sleep 30
salt-key -y -a `hostname`*
