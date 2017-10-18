#!/bin/sh
template=`cat <<TEMPLATE
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
SENDER=`cat /etc/ssmtp/ssmtp.conf  | grep 'AuthUser=' | sed -e 's/AuthUser=//'`
#SENDER="va-monitoring@mydomain.com"
/usr/bin/printf "%b" "$template"  | mail -a "From: $SENDER" -s "$NOTIFICATIONTYPE - $HOSTDISPLAYNAME - $SERVICEDISPLAYNAME is $SERVICESTATE" $USEREMAIL 
