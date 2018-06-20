#!/bin/sh
TEXT=`cat <<TEMPLATE
Notification Type: $NOTIFICATIONTYPE

Service: $SERVICEDESC
Host: $HOSTALIAS
Address: $HOSTADDRESS
State: $SERVICESTATE

Date/Time: $LONGDATETIME

Additional Info: $SERVICEOUTPUT

Comment: [$NOTIFICATIONAUTHORNAME] $NOTIFICATIONCOMMENT
TEMPLATE
`



SUBJECT="$NOTIFICATIONTYPE - $HOSTDISPLAYNAME - $SERVICEDISPLAYNAME is $SERVICESTATE"
PROJECT="vlatko"

if [ "$SERVICESTATE" = 'CRITICAL' ] 
		then
		PRIORITY="4"
elif [ "$SERVICESTATE" = 'WARNING' ] 
		then
		PRIORITY="3"
elif [ "$SERVICESTATE" = 'UNKNOWN' ] 
		then
		PRIORITY="2"
else
		PRIORITY="1" # SHOULD CLOSE THE TICKET
fi
# 1 LOW
# 2 NORMAL
# 3 HIGH
# 4 URGENT
# 5 IMMEDIATE

curl -H "X-Redmine-API-Key: MY_KEY" -H "Content-Type: application/xml"  -d "<?xml version="1.0"?><issue><project_id>$PROJECT</project_id><subject>$SUBJECT</subject><priority_id>$PRIORITY</priority_id><description>$TEXT</description></issue>
" https://MY_REDMINE_SERVER/issues.xml



