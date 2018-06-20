#!/bin/bash
#
# VA-PROXY RESTART SERVICES SCRIPT

#service icinga2 checkconfig > /dev/null
#OUT=$?
#if [ $OUT -eq 0 ];then
#   text="OK Config"
#else
#   exit 1
#fi


service squid3 stop
service e2guardian stop
sleep 10
service squid3 start
service e2guardian start
service e2guardian status
