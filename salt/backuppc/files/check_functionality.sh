#!/bin/sh
    #
# CHECK SCRIPT FOR VA-BACKUPPC

NOW=`echo $(date +"%s")`

exitstate=0
text="OK: "
CLEAN_OUT=`backuppc_servermsg status hosts | sed 's/,/,\n/g'| sed 's/},/\n/g'`
OLDEST=`echo "$CLEAN_OUT" | grep 'lastGoodBackupTime' | sed "s/.*=> //" | sed 's/,//'| sort -nr | tail -n 1 | awk '{print int($1)}'`
if [ -z "$OLDEST" ]; then
    OLDEST=$NOW
fi

GOODBACKUPS=`echo "$CLEAN_OUT" | grep 'lastGoodBackupTime' | wc -l`
TOTALBACKUPS=`echo "$CLEAN_OUT" | grep -E '"type" => "incr|full"' | wc -l`
FAILEDBACKUPS=`echo "$CLEAN_OUT" |  grep 'Reason_backup_failed' | wc -l`
RUNNING=`echo "$CLEAN_OUT" |  grep Status_backup_in_progress | wc -l`

EMPTYBACKUPS=`expr $TOTALBACKUPS - $GOODBACKUPS`
SPACE=`backuppc_servermsg status info | sed 's/,/,\n/g'| sed 's/},/\n/g' | grep "DUlastValue. =" | sed "s/.*=> //" | sed 's/,//'`

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

if [ $exitstate -lt "2" ]; then

	if [ "$FAILEDBACKUPS" -gt "2" ]; then
	    text='CRITICAL: ' 
		exitstate=2
	else
		if [ "$FAILEDBACKUPS" -gt "1" ]; then
			text='WARNING: ' 
			exitstate=1
		fi
	fi
fi

if [ $exitstate -lt "2" ]; then

	if [ "$EMPTYBACKUPS" -gt "2" ]; then
	    text='CRITICAL: ' 
		exitstate=2
	else
		if [ "$EMPTYBACKUPS" -gt "0" ]; then
			text='WARNING: ' 
			exitstate=1
		fi
	fi
fi

text=$text' Oldest backup is '$D' days, '$H' hours, '$M' minutes old. Currently running Jobs: '$RUNNING', Failed jobs: '$FAILEDBACKUPS', Total hosts: '$TOTALBACKUPS', Hosts without backup: '$EMPTYBACKUPS'. Used pool space: '$SPACE'%'
if [ -z "$SPACE" ]; then
text="Can not test functionality. Permissions issue"
exitstate=1
fi
echo $text" | exit_status="$exitstate
exit $exitstate
#604800 is one week in ms
