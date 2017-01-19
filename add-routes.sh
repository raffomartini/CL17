#!/bin/bash
gw=`netstat -nr | awk 'NR==1,/Internet6/{if (match($1,/default/) && match($6,/en4/)){ print $2}}'`
route -n add 10.100.0.0/16 $gw
route -n add 10.130.0.0/16 $gw


