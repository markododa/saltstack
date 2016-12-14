#!/bin/bash
set -e
if [ -z "$1" ]
then 
echo "The first argument should be the role"
exit
fi
if [ -n "$1" ]
then
ROLE=$1
fi
if [ `lsb_release -cs` == "jessie" ]; then
wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main' > /etc/apt/sources.list.d/salt.list
fi
if [ `lsb_release -cs` == "xenial" ]; then
wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' > /etc/apt/sources.list.d/salt.list
fi
apt-get update -y
apt-get install salt-minion -y
cd "$(dirname "$0")"
mkdir /srv/{salt,pillar,reactor,salt/_modules}
cp -R states/* /srv/salt
cp -R pillars/* /srv/pillar
cp -R reactor/* /srv/reactor
cp -R modules/* /srv/salt/_modules
echo "file_client: local" >> /etc/salt/minion
echo "role: $ROLE" > /etc/salt/grains
service salt-minion restart
#setup pillars
echo "Setup pillars and run salt-call --local state.highstate or salt-call --local state.apply"

