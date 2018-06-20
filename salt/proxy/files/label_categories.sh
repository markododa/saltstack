#!/bin/bash
#
# CREATE LABELS FOR EACH CATEGORY

echo ". "
for f in /etc/e2guardian/lists/blacklists/*; do

LABEL=`cat "$f""/domains" | grep '#listcategory:' | wc -l`
if [ $LABEL -eq 0 ];then
   CATEGORY=`echo "$f"  | sed -e 's/\/etc\/e2guardian\/lists\/blacklists\///'`
   echo '#listcategory: "'$CATEGORY'"' >> "$f"'/domains'
   echo "Fixing ""$f" 
else
   echo "$f"" is OK"
fi
done





