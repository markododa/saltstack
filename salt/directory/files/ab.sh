﻿#!/bin/sh
echo "Generating address book..."
domain=$(samba-tool domain info 127.0.0.1  | grep Domain | sed s'/Domain           : //')
lineno=1
rm /var/lib/samba/sysvol/addressbook.vcf
echo "\"Name\",\"E-mail Address\"" > /var/lib/samba/sysvol/addressbook.csv
pdbedit -Lv | grep 'Unix\|Full\|User SID' | sed s'/Unix username:        //'| sed s'/Full Name:            //' | sed s'/User SID:             //' | while read line;
do

case $lineno in
1)
lineno=2
onlyuser=$line
mail=$line"@"$domain
;;
2)
lineno=3
uuid=$line 
;;

3)
lineno=1
if [ $(echo $line | wc -c) = 1 ]; then
line=$onlyuser
else

if [ $(echo $line | grep '\$' | wc -c) = 0 ]; then
#Normal user
echo "\""$line"\",\""$mail"\""  >> /var/lib/samba/sysvol/addressbook.csv
					   
echo "BEGIN:VCARD" >> /var/lib/samba/sysvol/addressbook.vcf
echo "VERSION:3.0" >> /var/lib/samba/sysvol/addressbook.vcf
echo "N:;\"$line\";;;" >> /var/lib/samba/sysvol/addressbook.vcf
echo "FN:\"$line\""  >> /var/lib/samba/sysvol/addressbook.vcf
echo "EMAIL;TYPE=\"INTERNET,WORK\";PREF=1:$mail" >> /var/lib/samba/sysvol/addressbook.vcf
echo "UID:$uuid" >> /var/lib/samba/sysvol/addressbook.vcf
echo "END:VCARD" >> /var/lib/samba/sysvol/addressbook.vcf
echo " " >> /var/lib/samba/sysvol/addressbook.vcf
fi
fi
done
;;
sed -i s'/$/\r/' /var/lib/samba/sysvol/addressbook.csv
