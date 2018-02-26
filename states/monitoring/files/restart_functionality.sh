#!/bin/bash
#
# VA-MONITORING RESTART SERVICES SCRIPT

service icinga2 checkconfig > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text="OK Config"
else
   exit 1
fi


service icinga2 stop
service npcd stop
sleep 10
service icinga2 start
service npcd start 
service icinga2 status
