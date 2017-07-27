#!/bin/bash
# VA MASTER TEST

exitstate=0
text=""


OUT=`ps aux | grep python |grep va_master | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"VA-master process not running"
  exitstate=2
else
    text=$text"VA-master process is running"
fi


service openvpn status > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
   text=$text", VPN Server is OK"
else
   text=$text", VPN Server is DOWN"
   exitstate=1
fi

echo $text

exit $exitstate
