#!/bin/bash
set -e

if ! (  command lsb_release );then
        apt-get update
        apt-get -y install lsb-release
fi

version=$(lsb_release -cs)

if [ $version != "jessie" ] && [ $version != "xenial" ]; then
        echo "OS not supported"
        false
fi

if [ $version == "jessie" ]; then
wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main' > /etc/apt/sources.list.d/salt.list
fi

if [ $version == "xenial" ]; then
wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' > /etc/apt/sources.list.d/salt.list
fi


apt-get update -y
apt-get dist-upgrade -y
service salt-minion restart
