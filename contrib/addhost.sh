#!/bin/bash
#
# Usage: addhost $HOST $CHECKS


IPADDR=`nslookup hedwig | grep -i address | tail -1 | cut -f2 -d' '`

echo "[$1]"
echo "IPADDR=$IPADDR"
echo "CHECKINTERVAL=1"
echo "DESC=$1"
echo "COMMUNITY=public"
echo "COLLECTORS=$2"
echo ""

