#!/bin/sh
		printf_cmd="/usr/bin/printf"
		command_file="/var/run/icinga2/cmd/icinga2.cmd"
		hostname="$1"
		service="$2"
		now=`date +%s`
		#LOGGING AUTO ACKNOWLEDGE OF UNKNOWN WMIC STATES
		#$printf_cmd "[%lu] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;1;0;1;%s;%s\n" $now "$hostname" "$service" "OK" "AutoAck" >> /home/events.txt

case "$3" in
OK)
        # The service just came back up, so don't do anything...
        ;;
WARNING)
        # We don't really care about warning states, since the service is probably still running...
        ;;
UNKNOWN)
	#ACKNOWLEDGE_SVC_PROBLEM;<host_name>;<service_description>;<sticky>;<notify>;<persistent>;<author>;<comment>
	$printf_cmd "[%lu] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;1;0;1;%s;%s\n" $now "$hostname" "$service" " " "AutoAck" >> $command_file
        # We don't know what might be causing an unknown error, so don't do anything...
        ;;
CRITICAL)
        ;;
esac

