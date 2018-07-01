#!/bin/bash
if [ "$#" -ne 1 ]; then
	echo "Usage: open.sh [port]"
	exit
fi
nc -l -p $1 -vvv
