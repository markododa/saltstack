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
sleep 10
service icinga2 start
service icinga2 status
