#!/bin/bash
exitstate=0
TEXT_FILE=monitoring.txt
TXT=`cat $TEXT_FILE  | sed -e 's/\r//g' | grep "CPU;" `
SENSOR=`echo $TXT | cut -d';' -f 1`
OBJECT=`echo $TXT | cut -d';' -f 2`
UNIT=`echo $TXT | cut -d';' -f 3`
VALUE=`echo $TXT | cut -d';' -f 4`

#echo $SENSOR
#echo $OBJECT
#echo $UNIT
#echo $VALUE

OUT="OK"
if [ "$VALUE" -gt "80" ];then
OUT="WARNING"
exitstate=2
fi

if [ "$VALUE" -gt "90" ];then
OUT="CRITICAL"
exitstate=1
fi

echo  $OUT" - "$SENSOR" "$OBJECT" "$VALUE$UNIT" | cpu="$VALUE"%;80;90;"
exit $exitstate