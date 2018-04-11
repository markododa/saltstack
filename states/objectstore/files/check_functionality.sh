#!/bin/bash
#
# CHECK SCRIPT FOR VA-OBJECTSTORE

exitstate=0
text="OK"

# DENIED=`grep '*DENIED*' /var/log/e2guardian/access.log | wc -l`
# CHILDREN=`tail -n 1 /var/log/e2guardian/dstats.log | awk -v N=2 '{print $N}'`

# if [ $CHILDREN == "childs" ];then
# CHILDREN=`tail -n 2 /var/log/e2guardian/dstats.log | head -n 1 | awk -v N=2 '{print $N}'`
# fi


# MAXCHILDREN=`grep '^maxchildren' /etc/e2guardian/e2guardian.conf | sed -e 's/[^0-9]*\([0-9]*\)/\1/g'`
# PERCHIL=`awk -v m=$MAXCHILDREN -v c=$CHILDREN 'BEGIN { printf "%.0f", ( ( c / m ) * 100 ) }'`
# service squid3 status > /dev/null
# OUT=$?
# if [ $OUT -eq 0 ];then
#    text=$text"Squid Server is up"
# else
#    text=$text"Squid Server is DOWN"
#    exitstate=1
# fi

# service e2guardian status > /dev/null
# OUT=$?
# if [ $OUT -eq 0 ];then
#    text=$text", E2Guardian is up ("$CHILDREN"/"$MAXCHILDREN" children)"
# else
#    text=$text", E2Guardian is DOWN"
#    exitstate=1
# fi

# if [ $PERCHIL -gt 90 ];then
#    exitstate=2
# fi


echo $text" | exit_status="$exitstate

exit $exits
