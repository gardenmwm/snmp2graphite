#!/bin/bash
#Stops snmp2graphite

for i in `cat /opt/snmp2graphite/snmp2graphite.pids`; do
	kill -9 $i
done
