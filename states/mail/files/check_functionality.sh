#!/bin/bash
#
# CHECK SCRIPT FOR VA-OWNCLOUD

exitstate=0
text=""


#OUT=`sudo -u www-data /mnt/va-owncloud/owncloud/occ --version`
#text=$OUT":"

#OUT=`sudo -u www-data /mnt/va-owncloud/owncloud/occ ldap:show-remnants | wc -l`
#OUT=$(($OUT-4))
#if [ $OUT -eq 0 ];then
#    text=$text
#else
#	if [ $OUT -gt 3 ];then
#		text=$text', '"Ghost profiles: "$OUT
#		   exitstate=2
#	else
#		text=$text', '"Ghost profiles: "$OUT
#		   exitstate=1
#	fi
#fi

OUT=`service dovecot status | grep 'Active: active' | wc -l`
if [ $OUT -eq 0 ];then
    text=$text''"Dovecot DOWN"
   exitstate=2
else
    text=$text''"Dovecot is OK"
	#', '"Groups: $OUT"
fi

OUT=`service mysql status | grep 'Active: active' | wc -l`
if [ $OUT -eq 0 ];then
    text=$text', '"Postfix DOWN"
   exitstate=2
else
    text=$text','"Postfix is OK"
	#', '"Groups: $OUT"
fi




#OUT=`netstat -ntap |grep '1024' | wc -l`
#if [ $OUT -eq 0 ];then
#    text=$text', '"Replication port down!"
#   exitstate=2
#else
#    text=$text #', '"Replication port OK"
#fi



echo $text

exit $exitstate
