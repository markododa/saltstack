#!/bin/bash
#
# CHECK SCRIPT FOR VA-PROXY

exitstate=0
text=""

DENIED=`grep '*DENIED*' /var/log/e2guardian/access.log | wc -l`
CHILDREN=`tail -n 1 /var/log/e2guardian/dstats.log | awk -v N=2 '{print $N}'`
MAXCHILDREN=`grep '^maxchildren' /etc/e2guardian/e2guardian.conf | sed -e 's/[^0-9]*\([0-9]*\)/\1/g'`
PERCHIL=`awk -v m=$MAXCHILDREN -v c=$CHILDREN 'BEGIN { printf "%.1f", ( ( c / m ) * 100 ) }'`

#CHILCRIT=`awk -v m=$PERCHIL 'BEGIN { print (m > 90) ? "1" : "0" }'`
#exitstate=$CHILCRIT
#echo $CHILCRIT
service squid status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text"Squid Server is OK"
else
   text=$text"Squid Server is DOWN"
   exitstate=1
fi

service e2guardian status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text", E2Guardian is OK ("$CHILDREN"/"$MAXCHILDREN" children)"
else
   text=$text", E2Guardian is DOWN"
   exitstate=1
fi


echo $text" | BlockedToday="$DENIED", E2Gchildren="$CHILDREN", E2Gused="$PERCHIL"%;80%;90%"

exit $exitstate

