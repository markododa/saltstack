#!/bin/bash
#
# TOP ALLOWED

cat /var/log/e2guardian/access.log*  | grep -v '*DENIED*'|  grep -v '.jpg	'  | grep -v '.png	' | grep -v '.gif	'| cut -f 6 | cut --delimiter=/ -f 3 | sort | uniq -c | sort -nr
