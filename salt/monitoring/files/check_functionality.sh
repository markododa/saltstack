#!/bin/bash
#
# VA-MONITORING CHECK FUNCTIONALITY SCRIPT

exitstate=0
text=""


OUT=`cat /etc/ssmtp/ssmtp.conf | grep 'AuthPass=empty' | wc -l`
if [ $OUT -eq 1 ];then
   text=$text"Mail not configured. "
   exitstate=1
else
    text=$text""
fi

if [ -d /var/lib/pnp4nagios/perfdata/ ]; then
grep '<RC>' /var/lib/pnp4nagios/perfdata/* -R > /dev/null
if [ $? -eq 0 ];then

OUT=`grep '<RC>1' /var/lib/pnp4nagios/perfdata/* -R | wc -l`
if [ $OUT -eq 0 ];then
   text=$text""
else
   text=$text"Error in chart data. " 
   exitstate=1
fi



else
   text=$text"No chart data. " 
   exitstate=1
fi


service npcd status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text"Chart service is OK. "
else
   text=$text"Chart service is DOWN. "
   exitstate=2
fi
fi

service icinga2 status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text""
else
   text=$text"Monitoring service is DOWN! "
   exitstate=2
fi


text=$text"Last monitoring activity: "`TZ='Europe/Skopje' /bin/date +%Y-%m-%d" "%H:%M" "\(%Z\) -r /var/log/icinga2/icinga2.log`


echo $text" | exit_status="$exitstate

exit $exitstate
