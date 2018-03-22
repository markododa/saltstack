#!/bin/bash
#
# TOP ALLOWED

cat /var/log/e2guardian/access.log*  | grep -v '*DENIED*'|  grep -v '.jpg	'  | grep -v '.png	' | grep -v '.gif	'| awk -v N=4 '{print $N}' | awk -F/ '{print $3}' | sort | uniq -c | sort -nr | head -n 100
