#!/bin/bash
#
# CHECK SCRIPT FOR VA-FILESHARE

exitstate=0
text=""


OUT=`timeout 3 bash -c "smbclient -L localhost -N -d 0 -g | grep '^Disk|' | wc -l"`
text="Shared folders: "$OUT


OUT=`timeout 3 bash -c "smbclient -L localhost -N -d 0 -g | grep '^Printer|' | wc -l"`
text=$text", Shared printers: "$OUT



OUT=`timeout 10 bash -c "pdbedit -L | grep locked | wc -l"`
if [ $OUT -eq 0 ];then
   text=$text", No locked users"
else
    text=$text", Locked accounts: $OUT!"
   exitstate=1
fi

timeout 10 bash -c "smbclient -L localhost -N -d 0" > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Samba shares OK"
else
    text=$text', '"Samba shares problem!"
   exitstate=2
fi


timeout 10 bash -c "smbstatus -d 0" > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
    text=$text #', '"Samba status OK"
else
    text=$text', '"Samba status problem!"
   exitstate=2
fi

echo $text" | exit_status="$exitstate

exit $exitstate

