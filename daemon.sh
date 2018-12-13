#!/bin/bash

SERVER=""
USER=""
INTERVAL=0
COMMANDS=""

if [ $# == '0' ] ; then
    echo "No config file specified. Exiting." >&2; exit 1;
fi

if [ -f "$1" ] ; then
    . $1 #TODO: Not use native sourcing...
else
    echo "Config file not found. Exiting." >&2; exit 1;
fi

