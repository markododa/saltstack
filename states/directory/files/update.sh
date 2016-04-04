#!/bin/bash
user="$(echo $1| sed 's/.*smbd.*\\//' | cut -d'|' -f1)"
exist=$(cat /var/log/lastlogin.log | grep $(echo $1| sed 's/.*smbd.*\\//' | cut -d'|' -f1)| wc -c)
if [ "$exist" = "0" ]; then
#echo "new user"
echo "Jan  1 00:00:01 va-temp smbd_audit: TEMP\"$user""|8.8.8.8|connect|ok|sysvol">> /var/log/lastlogin.log
fi
#echo "replacing"
sed -i s"/.*\\""$(echo $1| sed 's/.*smbd.*\\//' | cut -d'|' -f1)""|.*/\\""$(echo $1| sed 's/\\/\\\\/')|""/" /var/log/lastlogin.log

