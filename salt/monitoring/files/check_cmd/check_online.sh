#!/bin/bash
#
# Nagios Plugin to check that a host is offline as expected. Displays a warning when [warn_count] out of [packet_count] packages were successful
#
# Usage: ./check_online_warning.sh $HOSTADDRESS$ $ARG1$ $ARG2$
#
# $ARG1$ = packet_count, $ARG2$ = warn_count
# 
# By Markus Walther <voltshock@gmail.com>
# 
# Version: 201608021514
pingresult=`ping -c 3 $2`
### pl
packetloss=`echo $pingresult | grep 'packet loss' | awk -F',' '{ print $3}' | awk '{ print $1}'` 
if [ ${packetloss//[-%]/} -ge 3 ]
	then
		echo "OK: PC is OFFILNE! (PL=$packetloss)"
		exit 1
	else
	    echo "OK: PC is online (PL=$packetloss)"
	    exit 1 
fi
