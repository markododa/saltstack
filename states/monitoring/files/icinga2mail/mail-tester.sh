#!/bin/sh
template='MONITORING REPORT'
template=$template`printf '\n\r'`
template=$template`printf '\n\r'`
template=$template`printf '\n\r'`
template=$template`service icinga2 status | grep 'Active: ' | sed -e 's/   Active: /STATUS: /'`
template=$template`printf '\n\r'`
template=$template`printf '\n\r'`
template=$template`icingacli monitoring list | sed -e 's/+-\|L-/-/g' | grep -v 'OK    - '`
template=$template`printf '\n\r'`

SENDER=`cat /etc/ssmtp/ssmtp.conf  | grep 'AuthUser=' | sed -e 's/AuthUser=//'`
#echo sending from $SENDER to $1
#echo $template
#/usr/bin/printf "%b" "$template"  | mail -a "From: $SENDER" -s "Monitoring Report" $USEREMAIL
/usr/bin/printf "%b" "$template"  | mail -a "From: $SENDER" -s "Monitoring Report" support@vapour-apps.com

