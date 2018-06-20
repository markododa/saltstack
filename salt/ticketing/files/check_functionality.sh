#!/bin/bash
#
# CHECK SCRIPT FOR VA-TICKETING


exitstate=0
text=""


OUT=`ps aux | grep redmine | grep Passenger | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"RedMine is up"
else
   text=$text"RedMine is DOWN"
   exitstate=2

fi


service apache2 status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text", Web Server is up"
else
   text=$text", Web Server is DOWN"
   exitstate=2
fi

service mysql status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text", SQL Server is up"
else
   text=$text", SQL Server is DOWN"
   exitstate=2
fi


echo $text" | exit_status="$exitstate

exit $exitstate
