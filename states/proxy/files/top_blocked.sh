#!/bin/bash
#
# TOP BLOCKED

cat /var/log/e2guardian/access.log* | grep '*DENIED*' | grep -v '.jpg	'  | grep -v '.png	' | grep -v '.gif	'| awk -v N=4 '{print $N}' | cut --delimiter=/ -f 3 | sort | uniq -c | sort -nr  | head -n 100
