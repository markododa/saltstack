#!/bin/bash
git pull
declare -a git_folders=(states modules reactor)
declare -a folders=(/srv/salt /srv/salt/_modules /srv/reactor)

for i in $(seq 0 2)
	do diff --brief -r ${git_folders[i]} ${folders[i]} -x _modules
done
