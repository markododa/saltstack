#!/bin/bash

CRED="-uroot"
DUMP="mysqldump $CRED --ignore-table=mysql.event"
PATEKA="/root/.va/backup"
DATE=`date +%Y%m%d-%H%M`
find $PATEKA -iname *.gz -mtime +180 -delete;

# Get a list of all databases
DATABASES=$(echo "SHOW DATABASES" | mysql $CRED | grep -v -E "Database|performance_schema|information_schema")

for DB  in $DATABASES; do
        FILENAME="$PATEKA/$DB-$DATE.sql.gz"
        $DUMP $DB | gzip > $FILENAME
done
