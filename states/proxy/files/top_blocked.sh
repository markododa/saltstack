#!/bin/bash
#

cat /var/log/e2guardian/access.log | grep '*DENIED*' | awk -v N=4 '{print $N}' | awk -F/ '{print $3}' | sort | uniq -c | sort -nr | head -n 50






