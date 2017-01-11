#!/bin/bash
if [ `lsb_release -cs` == "jessie" ]; then
wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main' > /etc/apt/sources.list.d/salt.list
fi
if [ `lsb_release -cs` == "xenial" ]; then
wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' > /etc/apt/sources.list.d/salt.list
fi
apt-get update -y
apt-get install --no-install-recommends salt-master -y
cd "$(dirname "$0")"
mkdir /srv/{salt,pillar,reactor,salt/_modules}
cp -R states/* /srv/salt
cp -R pillars/* /srv/pillar
cp -R reactor/* /srv/reactor
cp -R modules/* /srv/salt/_modules
#setup pillars
#cp *.sls /srv/pillar
#cp /srv/salt/salt-master/files/master /etc/salt/master 
#service salt-master restart
apt-get install salt-minion -y
echo "master: localhost" >> /etc/salt/minion
echo "role: va-master" > /etc/salt/grains
service salt-minion restart
sleep 30
salt-key -y -a `hostname`
#tail -f -q /var/log/salt/minion |GREP_COLOR='1;32' grep -o "Completed state.*$" --color=always & salt-call --local state.highstate --log-file-level all -l quiet > /dev/null && pkill -f "tail -f -q /var/log/salt/minion"
