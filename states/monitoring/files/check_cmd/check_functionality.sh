#!/bin/bash
#
# GENERIC CHECK FUNCTIONALITY SCRIPT, SHOULD BE REPLACED WITH MACHINE SPECIFIC SCRIPT.


#/usr/lib/nagios/plugins/check_functionality.sh:
#  file.managed:
#    - source:
#      - salt://XXXX/files/check_functionality.sh
#    - user: root
#    - group: root
#    - mode: 755


exitstate=0
text=""


OUT=`cat /etc/ssmtp/ssmtp.conf | grep 'AuthPass=mailPASS' | wc -l`
if [ $OUT -eq 1 ];then
   text=$text"No config for mail notifications! "
   exitstate=1
else
    text=$text""
fi



OUT=`grep '<RC>1' /var/lib/pnp4nagios/perfdata/* -R | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"Charts data are OK. "
else
   text=$text"Error in chart data. " 
   exitstate=1
fi

text=$text"Last log entry: "`TZ='Europe/Skopje' /bin/date +%Y-%m-%d" "%H:%M" "\(%Z\) -r /var/log/icinga2/icinga2.log`


echo $text

exit $exitstate
