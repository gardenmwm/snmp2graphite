#!/bin/bash
#Start snmp2graphite

nohup python /opt/snmp2graphite/snmp2graphite.py &
sleep 1 
 ps -ef | grep snmp2graphite.py | grep -v grep | sed 's/  */,/g' | cut -f2 -d, > snmp2graphite.pids

