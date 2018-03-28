#!/bin/bash
#
# TOP BLOCKED

cat /var/log/e2guardian/access.log* | grep '*DENIED*' | grep -v '.jpg	'  | grep -v '.png	' | grep -v '.gif	'| cut -f 6 | cut --delimiter=/ -f 3 | sort | uniq -c | sort -nr  | head -n 100
