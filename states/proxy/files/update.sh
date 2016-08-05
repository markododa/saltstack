#this file generates ipgroups file that is needed for e2guardian
#Users in the group VA-Proxy VIP are privileged
#this script is run from va-directory in addition to update.sh for lastlogin 
user=$(echo $1 | cut -d'\' -f2| cut -d'|' -f1)
ip=$(echo $1 | cut -d'\' -f2| cut -d'|' -f2)
samba-tool group listmembers 'VA-Proxy VIP' > vip.txt
if grep -Fx $user vip.txt
then
    #echo "VIP user"
	line=$ip' = filter2 #'$user'#'
	if grep -q "$ip =" ipgroups ; then
		sed -i s"/$ip =.*$/$line/g" ipgroups
		else
		#echo 'new IP'
		echo $line >> ipgroups
	fi

else
    #echo "STD user"
	line=$ip' = filter1 #'$user'#'
	if grep -q "$ip =" ipgroups ; then
		sed -i s"/$ip =.*$/$line/g" ipgroups
		else
		#echo 'new IP'
		echo $line >> ipgroups
	fi
fi


 