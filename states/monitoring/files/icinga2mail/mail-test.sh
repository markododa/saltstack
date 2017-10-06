#!/bin/sh
template=`cat <<TEMPLATE
Test Mail
TEMPLATE
`
SENDER=`cat /etc/ssmtp/ssmtp.conf  | grep 'AuthUser=' | sed -e 's/AuthUser=//'`
echo sending from $SENDER to $1
/usr/bin/printf "%b" "$template"  | mail -a "From: $SENDER" -s "Monitoring test message" $1

