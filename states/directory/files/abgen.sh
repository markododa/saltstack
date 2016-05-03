#!/bin/sh
echo "Generating address book..."
domain=$(samba-tool domain info 127.0.0.1  | grep Domain | sed s'/Domain           : //')
lineno=1
rm /root/contacts/* -f
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
echo "\""$line"\",\""$mail"\"\r"  >> /var/lib/samba/sysvol/addressbook.csv
echo "BEGIN:VCARD\r" > /root/contacts/$uuid.vcf
echo "VERSION:3.0\r" >> /root/contacts/$uuid.vcf
echo "N:;$line;;;\r" >> /root/contacts/$uuid.vcf
echo "FN:$line\r"  >> /root/contacts/$uuid.vcf
echo "EMAIL;TYPE=\"INTERNET,WORK\";PREF=1:$mail\r" >> /root/contacts/$uuid.vcf
echo "UID:"$uuid"\r" >> /root/contacts/$uuid.vcf
echo "END:VCARD\r" >> /root/contacts/$uuid.vcf
#echo " " >> /var/lib/samba/sysvol/addressbook.vcf
fi
fi
;;
esac
done
sed -i s'/$/\r/' /var/lib/samba/sysvol/addressbook.csv
#sed -i s'/$/\r/' /var/lib/samba/sysvol/addressbook.vcf
