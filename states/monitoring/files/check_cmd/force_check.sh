#!/bin/sh
		printf_cmd="/usr/bin/printf"
		command_file="/var/run/icinga2/cmd/icinga2.cmd"
		hostname="$1"
		service="$2"
		now=`date +%s`
       # SCHEDULE_FORCED_SVC_CHECK;my pc;AD DNS A Records;1525798118
	$printf_cmd "[%lu] SCHEDULE_FORCED_SVC_CHECK;%s;%s;%s\n" $now "$hostname" "$service" "$now" >> $command_file
