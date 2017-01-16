#!/bin/bash
#
# GENERIC CHECK FUNCTIONALITY SCRIPT, SHOULD BE REPLACED WITH MACHINE SPECIFIC SCRIPT.


#/usr/lib/nagios/plugins/check_functionality.sh:
#  file.managed:
#    - source:
#      - salt://XXXX/files/check_functionality.sh
#    - user: root
#    - group: root
#    - mode: 755

exitstate=0
text="There is no functionality test script for this machine"



echo $text

exit $exitstate
