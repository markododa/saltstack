#!/bin/bash
#
# CHECK SCRIPT FOR VA-OBJECTSTORE

exitstate=0
text=""

OUT=`ps aux | grep /opt/minio/minio | grep -v grep | wc -l`
if [ $OUT -eq 0 ];then
   text=$text"Minio not running"
  exitstate=2
else
    text=$text"Minio is running"
fi



echo $text" | exit_status="$exitstate

exit $exits
