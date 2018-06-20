#!/bin/bash
user=`echo $1 | sed -e s/.*smbd_audit\:\ // -e s/\|.*// -e s'#\\\#\\\\\\\#'`
string=`echo $1 | sed s'#\\\#\\\\\\\#'`
echo $user
if grep -q "$user" /var/log/lastlogin.log ; then
  sed -i s"/^.*$user.*$/$string/g" /var/log/lastlogin.log
else
  echo $1 >> /var/log/lastlogin.log
fi
