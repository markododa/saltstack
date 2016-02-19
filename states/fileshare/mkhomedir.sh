#!/bin/bash

if [ ! -e /home/DOMAIN/$1 ]; then
	mkdir /home/DOMAIN/$1
	chown $1:"Domain Users" /home/DOMAIN/$1
fi
exit 0