#!/bin/bash
#
# CHECK SCRIPT FOR VA-MAIL

exitstate=0
text=""


OUT=`postqueue -p | tail -n 1 | sed 's/^-- //g' | awk '{ print $4}'`
if [ $OUT -le 5 ];then
    text=$text"Queue: "$OUT" messages"
else

 if [ $OUT -ge 25 ];then
    text=$text"Queue: "$OUT" messages (critical)"
    exitstate=2
 else
    text=$text"Queue: "$OUT" messages (warning)"
    exitstate=1
 fi
fi


service dovecot status > /dev/null
if [ $? -eq 0 ];then
    text=$text", Dovecot is OK"
else
    text=$text", Dovecot is DOWN"
    exitstate=2
fi

service postfix status > /dev/null
if [ $? -eq 0 ];then
    text=$text", Postfix is OK"
else
    text=$text", Postfix is DOWN"
   exitstate=2

fi

service clamav-daemon status > /dev/null
if [ $? -eq 0 ];then
    text=$text", ClamAV is OK"
else
    text=$text", ClamAV is DOWN"
   exitstate=2

fi

amavisd-new testkeys  > /dev/null
if [ $? -eq 0 ];then
    text=$text", DKIM is OK"
else
    text=$text", DKIM is DOWN"
   exitstate=2

fi

#queue_id='^[A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9]'
#queue_id='^(?:[0-9A-F]{10,11}|[0-9A-Za-z]{14,16})!\s'

# determine queue size
#OUT=$(mailq | egrep -c $queue_id)
#if [ -z $qsize ]
#then
#    exit $e_unknown
#fi


echo $text

exit $exitstate
