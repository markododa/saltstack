#!/bin/bash
git pull
declare -a git_folders=(salt reactor)
declare -a folders=(/srv/salt /srv/reactor)

for i in $(seq 0 1)
	do diff --brief -r ${git_folders[i]} ${folders[i]}
done
