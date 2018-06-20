#!/bin/bash
#
# LAST BLOCKED
 
cat /var/log/e2guardian/access.log | grep '*DENIED*' | grep -v '.jpg	'  | grep -v '.png	' | grep -v '.gif	'| cut -f 1,4,5,6,18,19 
