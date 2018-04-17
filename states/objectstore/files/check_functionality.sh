#!/bin/bash
#
# CHECK SCRIPT FOR VA-OBJECTSTORE

exitstate=0
text=""
PROBLEMS=0

OUT=`ps aux | grep /opt/minio/minio | grep -v grep | wc -l`
if [ $OUT -eq 0 ];then
    text=$text"Minio not running"
    exitstate=2
else
    text=$text"Minio is running"
fi

OUT=`find /opt/minio/data -iname sync.log | grep ".sysconfig/sync.log" | grep -v ".minio.sys" | wc -l`
if [ $OUT -eq 0 ];then
    t=""
else
    text=$text", Sync logs found: "$OUT
    text=$text", Clients with problems: "
    
    
    # CHECK FOR OLD ONES
    
    OUT=`find /opt/minio/data -iname sync.log -mmin +3 | grep ".sysconfig/sync.log" | grep -v ".minio.sys" | wc -l`
    PROBLEMS=$OUT
    
    if [ $OUT -eq 0 ];then
        t=""
    else
        OUT2=`find /opt/minio/data -iname sync.log -mmin +3 | grep ".sysconfig/sync.log" | grep -v ".minio.sys"`
        
        
        for f in $OUT2
        do
            CLIENT=`echo $f | sed -e 's/\/opt\/minio\/data\///g' | sed -e 's/.sysconfig\/sync.log//g'`
            
            text=$text$CLIENT" (Outdated), "
            exitstate=1
            
        done
        
    fi
    
    
    # IF NOT OLD CHECK FOR ERRORS
    OUT=`find /opt/minio/data -iname sync.log -mmin -3 | grep ".sysconfig/sync.log" | grep -v ".minio.sys" | wc -l`
    if [ $OUT -eq 0 ];then
        t=""
    else
        
        OUT=`find /opt/minio/data -iname sync.log -mmin -3 | grep ".sysconfig/sync.log" | grep -v ".minio.sys"` 
        for f in $OUT
        do
            TEST=`cat $f | grep "ERROR" | wc -l`
            CLIENT=`echo $f | sed -e 's/\/opt\/minio\/data\///g' | sed -e 's/.sysconfig\/sync.log//g'`
            if [ $TEST -eq 0 ];then
                t=""
            else
                PROBLEMS=$(($PROBLEMS +1))
                text=$text$CLIENT" (Error), "
                exitstate=1
            fi
        done
    fi
    
fi

echo $text" | exit_status="$exitstate"; err_clients="$PROBLEMS";0;0;"
#echo $PROBLEMS
exit $exitstate
