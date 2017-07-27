#!/bin/bash
# VA MASTER TEST
exitstate=0
text=""


OUT=`cat /etc/ssmtp/ssmtp.conf | grep 'AuthPass=mailPASS' | wc -l`
if [ $OUT -eq 1 ];then
   text=$text"No config for mail notifications! "
   exitstate=1
else
    text=$text""
fi

text=$text"Last log entry: "`/bin/date +%Y-%m-%d" "%H:%M" "\(%Z\) -r /var/log/icinga2/icinga2.log`


echo $text

exit $exitstate

