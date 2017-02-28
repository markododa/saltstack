#!/bin/bash
#
# CHECK SCRIPT FOR VA-DIRECTORY

exitstate=0
text=""


OUT=`sudo pdbedit -L | grep 'administratively locked out' | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"No locked users"
else
    text=$text"Locked accounts: $OUT!"
   exitstate=1
fi

OUT=`wbinfo -u | wc -l`
if [ $OUT -eq 0 ];then
    text=$text', '"No users!"
   exitstate=2
else
    text=$text', '"Users: $OUT"
fi

OUT=`wbinfo -g | wc -l`
if [ $OUT -eq 0 ];then
    text=$text', '"No groups!"
   exitstate=2
else
    text=$text', '"Groups: $OUT"
fi

OUT=`getent passwd | wc -l`
if [ $OUT -eq 0 ];then
    text=$text', '"No local users!"
   exitstate=2
else
    text=$text', '"Unix users: $OUT"
fi


OUT=`netstat -ntap |grep '1024' | wc -l`
if [ $OUT -eq 0 ];then
    text=$text', '"Replication port down!"
   exitstate=2
else
    text=$text #', '"Replication port OK"
fi


sudo samba-tool dbcheck -d 0  > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Data Base OK"
else
    text=$text', '"Database corrupted!"
   exitstate=2
fi


sudo samba-tool drs kcc -d 0 > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Consistency OK"
else
    text=$text', '"Consistency problem!"
   exitstate=2
fi

sudo samba-tool drs showrepl -d 0 > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Replication OK"
else
    text=$text', '"Replication problem!"
   exitstate=2
fi


smbclient -L localhost -N -d 0 > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Samba shares OK"
else
    text=$text', '"Samba shares problem!"
   exitstate=2
fi


smbstatus -d 0 > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Samba status OK"
else
    text=$text', '"Samba status problem!"
   exitstate=2
fi

DNS1=`nslookup $(hostname) | grep 'Address: ' | md5sum | awk -F " " '{print $1}'`
DNS2=`nslookup $(samba-tool domain info 127.0.0.1 | grep 'DC name          :'| sed -e "s/DC name          : //") | grep 'Address: '| md5sum | awk -F " " '{print $1}'`

if [[ $DNS1 == $DNS2 ]]; then
    text=$text #', '"Samba status OK"
else
    text=$text', '"Wrong DNS record for this DC!"
   exitstate=2
fi

echo $text

exit $exitstate

