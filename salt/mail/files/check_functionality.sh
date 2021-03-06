#!/bin/bash
#
# CHECK SCRIPT FOR VA-MAIL

exitstate=0
text=""


OUT=`postqueue -p | tail -n 1 | sed 's/^-- //g' | awk '{ print $4}'`
if [ $OUT = "empty" ];then
OUT=0
fi
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

OUT=`amavisd-new testkeys | grep ' => invalid' | wc -l`
if [ $OUT -eq 0 ];then
    text=$text", DKIM is OK"
else
    text=$text", invalid public DKIM record"
   exitstate=1

fi


echo $text" | exit_status="$exitstate

exit $exitstate
