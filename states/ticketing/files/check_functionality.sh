#!/bin/bash
#
# CHECK SCRIPT FOR VA-TICKETING

exitstate=0
text=""

OUT=`sudo pdbedit -Lv | grep 'administratively locked out' | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"No locked users"
else
    text=$text"Locked accounts: $OUT!"
   exitstate=1
fi


echo $text

exit $exitstate
