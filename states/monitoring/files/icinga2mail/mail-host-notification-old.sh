#!/bin/sh
template=`cat <<TEMPLATE
Notification Type: $NOTIFICATIONTYPE

Host: $HOSTALIAS
Address: $HOSTADDRESS
State: $HOSTSTATE

Date/Time: $LONGDATETIME

Additional Info: $HOSTOUTPUT

Comment: [$NOTIFICATIONAUTHORNAME] $NOTIFICATIONCOMMENT
TEMPLATE
`
SENDER=`cat /etc/ssmtp/ssmtp.conf  | grep 'AuthUser=' | sed -e 's/AuthUser=//'`
#SENDER="va-monitoring@mydomain.com"
/usr/bin/printf "%b" "$template" | mail -a "From: $SENDER" -s "$NOTIFICATIONTYPE - $HOSTDISPLAYNAME is $HOSTSTATE" $USEREMAIL
