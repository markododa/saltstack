#! /bin/sh
ldbsearch --cross-ncs -H /var/lib/samba/private/sam.ldb '(fsmoroleowner=*)' | grep 'dn:\|Role' | sed 's/CN=//g' |\
 sed 's/,Servers,.*//'|\
 sed 's/NTDS Settings,//'|\
 sed 's/fSMORoleOwner: //'|\
 sed 's/dn: //'|\
 sed 's/DC=//g'

 
echo "samba-tool fsmo transfer --role=all"
samba-tool fsmo show