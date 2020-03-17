#!/bin/bash
git pull
declare -a git_folders=(salt reactor)
declare -a folders=(/srv/salt /srv/reactor)

for i in $(seq 0 1)
	do diff -ru ${git_folders[i]} ${folders[i]}| grep -E '\-\-\- |\+\+\+ '
done
