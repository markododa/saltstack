#!/bin/bash
export SALTTREE=salt-tree.tar.gz
wget -O - https://repo.saltstack.com/apt/debian/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian jessie contrib' > /etc/apt/sources.list.d/salt.list
apt-get update
apt-get install --no-install-recommends salt-master
tar xzfv $SALTTREE -C /srv
cp /srv/salt/state/monitoring/files/master /etc/salt/master
service salt-master restart
apt-get install salt-minion
echo "master: $(hostname -f)" >> /etc/salt/minion
echo "role: monitoring" >> /etc/salt/grains
service salt-minion restart
salt '*' state.highstate
