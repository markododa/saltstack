#!/bin/bash
exitstate=0
TEXT_FILE=monitoring.txt
TXT=`cat $TEXT_FILE  | sed -e 's/\r//g' | grep "Memory;Free" `
SENSOR1=`echo $TXT | cut -d';' -f 1`
OBJECT1=`echo $TXT | cut -d';' -f 2`
UNIT1=`echo $TXT | cut -d';' -f 3`
VALUE1=`echo $TXT | cut -d';' -f 4`
VALUE1=$(( $VALUE1 / 1024))
TXT=`cat $TEXT_FILE  | sed -e 's/\r//g' | grep "Memory;Total" `
SENSOR2=`echo $TXT | cut -d';' -f 1`
OBJECT2=`echo $TXT | cut -d';' -f 2`
UNIT2=`echo $TXT | cut -d';' -f 3`
VALUE2=`echo $TXT | cut -d';' -f 4`
VALUE2=$(( $VALUE2 /1024/1024))
PERC=$((($VALUE2-$VALUE1)*100 / $VALUE2))
# echo $SENSOR1
# echo $OBJECT1
# echo $UNIT1
# echo $VALUE1
# echo $VALUE2
# echo $PERC

OUT="OK"
if [ "$PERC" -gt "80" ];then
OUT="WARNING"
exit=2
fi

if [ "$PERC" -gt "90" ];then
OUT="CRITICAL"
exit=1
fi

echo  $OUT" - "$SENSOR1" "$OBJECT1" "$VALUE1"MB, "$SENSOR2" "$OBJECT2$" "$VALUE2"MB | mem="$PERC"%;80;90; free="$VALUE1".0"
exit $exitstate