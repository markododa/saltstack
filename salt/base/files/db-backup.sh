#!/bin/bash

CRED="-uroot"
DUMP="mysqldump $CRED --ignore-table=mysql.event"
PATEKA="/root/.va/backup"
DATE=`date +%Y%m%d-%H%M`
find $PATEKA -mtime +180 -exec rm {} \;

# Get a list of all databases
DATABASES=$(echo "SHOW DATABASES" | mysql $CRED | grep -v Database | grep -v performance_schema | grep -v information_schema)

for DB  in $DATABASES; do
        FILENAME="$PATEKA/$DB-$DATE.sql.gz"
        $DUMP $DB | gzip > $FILENAME
done
