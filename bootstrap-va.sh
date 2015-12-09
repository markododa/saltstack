#!/bin/bash
#export SALTTREE=salt-tree.tar.gz
wget -O - https://repo.saltstack.com/apt/debian/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/latest jessie main' > /etc/apt/sources.list.d/salt.list
apt-get update
apt-get install --no-install-recommends salt-master
#tar xzfv $SALTTREE -C /srv
mkdir /srv/{salt,pillar}
cp -R states/* /srv/salt
cp -R pillars/* /srv/pillar
#setup pillars
cp /srv/salt/salt-master/files/master /etc/salt/master
service salt-master restart
apt-get install salt-minion
echo "master: `hostname -f`" >> /etc/salt/minion
echo "role: va-monitoring" >> /etc/salt/grains
service salt-minion restart
salt-key -y -a `hostname -f`
salt '*' state.highstate
