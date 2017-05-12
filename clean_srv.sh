#!/bin/bash
for x in $(./chkslt.sh |grep "Only in /srv"| cut -d " " -f 3,4 |sed s"#: #/#"); do rm $x; done
