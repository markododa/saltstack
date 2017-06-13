#!/bin/sh
#
# CHECK SCRIPT FOR VA-BACKUPPC

exitstate=0
text="OK: "

OLDEST=`cat /var/lib/backuppc/log/status.pl | grep "lastGoodBackupTime" | sed 's/    "lastGoodBackupTime" => //' | sed 's/,//'| sort -nr | head -n 1 | awk '{print int($1)}'`
SPACE=`cat /var/lib/backuppc/log/status.pl | grep '"DUlastValue" =>' | sed 's/  "DUlastValue" => //'  | sed 's/,//'`
TOTALERRORS=`cat /var/lib/backuppc/log/status.pl | grep '"error" => "' | wc -l`
NOW=`echo $(date +"%s")`
#echo $OLDEST
#echo $NOW
T=`expr $NOW - $OLDEST`
D=$((T/60/60/24))
H=$((T/60/60%24))
M=$((T/60%60))
#S=$((T%60))

if [ "$D" -gt "7" ]; then
    text='CRITICAL: ' 
	exitstate=2
else
	if [ "$D" -gt "2" ]; then
		text='WARNING: ' 
		exitstate=1
	fi
fi

if [ "$TOTALERRORS" -gt "2" ]; then
    text='CRITICAL: ' 
        exitstate=2
else
        if [ "$TOTALERRORS" -gt "1" ]; then
                text='WARNING: ' 
                exitstate=1
        fi
fi

text=$text' Last good backup is '$D' days, '$H' hours, '$M' minutes old. Total errors:'$TOTALERRORS'. Used pool space: '$SPACE'%'
echo $text
exit $exitstate
#604800 is one week in ms
