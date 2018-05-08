#!/bin/bash

#set these in your environment/profile (NOT HERE)

$OBJSERVER=$1
$WINCLIENT=$2
AWS_ACCESS_KEY="---------JTIZSL08YCAZ" 
AWS_SECRET_KEY="----------sNyb3Q"

ACCESS_KEY=`cat /etc/icinga2/conf/$OBJSERVER.objectstore  | grep 'ACCESS_KEY=' | sed -e 's/ACCESS_KEY=//'`
SECRET_KEY=`cat /etc/icinga2/conf/$OBJSERVER.objectstore  | grep 'SECRET_KEY=' | sed -e 's/SECRET_KEY=//'`
#example usage
#s3get my-bucket/a/path/to/my/file > /tmp/file

    function fail { echo "$1" > /dev/stderr; exit 1; }

    #dependency check
    if ! hash openssl 2>/dev/null; then fail "openssl not installed"; fi
    if ! hash curl 2>/dev/null; then fail "curl not installed"; fi
    #params
    path="$WINCLIENT.sysconf/monitoring.txt"
    bucket=$(cut -d '/' -f 1 <<< "$path")
    key=$(cut -d '/' -f 2- <<< "$path")
    region="${2:-us-east-1}"
    #load creds
    access="$ACCESS_KEY"
    secret="$SECRET_KEY"
    #validate
    if [[ "$bucket" = "" ]]; then fail "missing bucket (arg 1)"; fi;
    if [[ "$key" = ""    ]]; then fail "missing key (arg 1)"; fi;
    if [[ "$region" = "" ]]; then fail "missing region (arg 2)"; fi;
    if [[ "$access" = "" ]]; then fail "missing AWS_ACCESS_KEY (env var)"; fi;
    if [[ "$secret" = "" ]]; then fail "missing AWS_SECRET_KEY (env var)"; fi;
    #compute signature
    contentType="text/html; charset=UTF-8" 
    date="`date -u +'%a, %d %b %Y %H:%M:%S GMT'`"
    resource="/${bucket}/${key}"
    string="GET\n\n${contentType}\n\nx-amz-date:${date}\n${resource}"
    signature=`echo -en $string | openssl sha1 -hmac "${secret}" -binary | base64` 
#    echo $signature
    #get!
    curl -H "x-amz-date: ${date}" \
        -H "Content-Type: ${contentType}" \
        -H "Authorization: AWS ${access}:${signature}" \
        "https://va-objectstore.-----.va.mk${resource}"
