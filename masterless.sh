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

if ! (  command lsb_release );then
        apt-get update
        apt-get -y install lsb-release wget gnupg
fi


version=$(lsb_release -cs)

if [ $version != "jessie" ] && [ $version != "xenial" ] && [ $version != "stretch" ]; then
        echo "OS not supported"
        false
fi

if [ $version == "jessie" ]; then
wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main' > /etc/apt/sources.list.d/salt.list
fi

if [ $version == "stretch" ]; then
wget -O - https://repo.saltstack.com/apt/debian/9/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/9/amd64/latest stretch main' > /etc/apt/sources.list.d/salt.list
fi

if [ $version == "xenial" ]; then
wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' > /etc/apt/sources.list.d/salt.list
fi

apt-get update -y
apt-get install salt-minion -y
cd "$(dirname "$0")"
mkdir /srv/{pillar,reactor}
cp -R salt /srv/
cp -R pillar/* /srv/pillar
cp -R reactor/* /srv/reactor
echo "file_client: local" >> /etc/salt/minion
echo "role: $ROLE" > /etc/salt/grains
service salt-minion restart
#setup pillars
echo "Setup pillars and run salt-call --local state.highstate or salt-call --local state.apply"

