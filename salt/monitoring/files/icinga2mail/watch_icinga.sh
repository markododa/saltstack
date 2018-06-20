#!/bin/bash
NEWCRC=`tail /var/log/icinga2/icinga2.log | md5sum | awk -F " " '{print $1}'`
OLDCRC=`cat /root/.va/icingaCRC.txt | awk -F " " '{print $1}'`

echo $OLDCRC
echo $NEWCRC

    if [[ $NEWCRC == $OLDCRC ]]; then

	/usr/sbin/service icinga2 stop
	sleep 10
	/usr/sbin/service icinga2 start 
#	date >> /home/icingaRestart.txt
    else
        echo "ICINGA OK"
    fi

echo $NEWCRC > /root/.va/icingaCRC.txt

