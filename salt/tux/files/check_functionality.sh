#!/bin/bash
#
# CHECK SCRIPT FOR VA-TUX

exitstate=0
text=""
PROBLEMS=0

#OUT=`ps aux | grep processname | grep -v grep | wc -l`
#if [ $OUT -eq 0 ];then
#    text=$text"Process not running"
#    exitstate=2
#else
#    text=$text"Process is running"
#fi

echo $text" | exit_status="$exitstate"; err_clients="$PROBLEMS";0;0;"
exit $exitstate
