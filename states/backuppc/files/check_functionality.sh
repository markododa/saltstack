#!/bin/sh
#
# CHECK SCRIPT FOR VA-BACKUPPC

exitstate=0
text="OK: "
OLDEST=`backuppc_servermsg status hosts | sed 's/,/,\n/g'| sed 's/},/\n/g'| grep 'lastGoodBackupTime' | sed "s/.*=> //" | sed 's/,//'| sort -nr | tail -n 1 | awk '{print int($1)}'`
SPACE=`backuppc_servermsg status info | sed 's/,/,\n/g'| sed 's/},/\n/g' | grep "DUlastValue. =" | sed "s/.*=> //" | sed 's/,//'`
TOTALBACKUPS=`backuppc_servermsg status hosts | sed 's/,/,\n/g'| sed 's/},/\n/g' | grep reason | wc -l`
FAILEDBACKUPS=`backuppc_servermsg status hosts | sed 's/,/,\n/g'| sed 's/},/\n/g' |  grep 'Reason_backup_failed' | wc -l`
RUNNING=`backuppc_servermsg status hosts | sed 's/,/,\n/g'| sed 's/},/\n/g' | grep Status_backup_in_progress | wc -l`
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

if [ "$FAILEDBACKUPS" -gt "2" ]; then
    text='CRITICAL: ' 
        exitstate=2
else
        if [ "$FAILEDBACKUPS" -gt "1" ]; then
                text='WARNING: ' 
                exitstate=1
        fi
fi

text=$text' Oldest backup is '$D' days, '$H' hours, '$M' minutes old. Currently running Jobs: '$RUNNING', Failed jobs: '$FAILEDBACKUPS', Total hosts to backup: '$TOTALBACKUPS'. Used pool space: '$SPACE'%'
if [ -z "$SPACE" ]; then
text="Can not test functionality"
fi
echo $text" | exit_status="$exitstate
exit $exitstate
#604800 is one week in ms
