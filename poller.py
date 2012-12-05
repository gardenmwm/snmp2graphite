'''
Created on Jun 27, 2012

@author: marsham
'''

from netsnmp import snmpwalk
import time
import sys
import multiprocessing
from multiprocessing import Queue
import graphitesender
debug = 1

CollectorQueue = Queue()
exitFlag = 0
collectorpool = []

'''
COLLECTOR = {"DESC":"Load",
             "TYPE":"table",
             "MIBDESC":".1.3.6.1.4.1.2021.10.1.2",
             "MIBDATA":".1.3.6.1.4.1.2021.10.1.3",
             "NAMING_SCHEMA": 'snmp.%HOST%.%COLLECTOR%.%MIB%'
             }


HOST = { "DESC":"HSProd11",
        "IPADDR":"159.36.2.146",
        "COMMUNITY":"public",
        "INTERVAL":1,
        "COLLECTORS":["load"]
        }

NAMING_SCHEMA = 'snmp.%HOST%.%COLLECTOR%.%MIB%'
'''
COLLECTORS = {}

def Collector(host, collector):
    """
    Collector that gets snmp data
    """
    if debug:print "Collector for %s %s" % (host['DESC'], collector['DESC'])
    results = []
    mibs = dict(zip(collector['MIBDESC'], collector['MIBDATA']))
    if collector["TYPE"] == "multi":
        for k, v in mibs.iteritems():
            description = collector["NAMING_SCHEMA"].replace('$HOST$', host['DESC']).replace('$COLLECTOR$', collector['DESC']).replace('$MIB$', k)
            results.append(GetSNMPValue(host['IPADDR'], host['COMMUNITY'], v, description))
    elif collector["TYPE"] == "table":
        results = GetSNMPValueTable(host, collector)
    if results == None: results = 'NoData'
    if debug:print "Results from collector for %s %s: %s" % (host['DESC'],collector['DESC'],results)
    return results

def GetSNMPValue(host, community, mib, desc):
    """
    Gets the SNMP value for a given mib
    """
    if debug: print "GetSNMPVal for %s %s" % (host, desc)
    now = int(time.time())
    try:
        value = snmpwalk(mib, Version = 2, DestHost = host, Community = community)[0]
        return [desc, value, now]
    except:
        print "SNMP ISSUES with %s using %s" % (host, desc)
        return "NoData"

def GetSNMPValueTable(host, collector):
    """
    Gets the SNMP values for Table MIBS
    """
    if debug:print "GetSNMPValueTable for %s %s" % (host['DESC'], collector['DESC'])
    mibdesc = collector['MIBDESC']
    mibdata = collector['MIBDATA']
    community = host['COMMUNITY']
    ipaddr = host['IPADDR']
    now = int(time.time())
    try:
        desc = snmpwalk(mibdesc, Version = 2, DestHost = ipaddr, Community = community)
        vals = snmpwalk(mibdata, Version = 2, DestHost = ipaddr, Community = community)
        results = []
        for i in range(len(desc)):
            description = collector["NAMING_SCHEMA"].replace('$HOST$', host['DESC']).replace('$COLLECTOR$', collector['DESC']).replace('$MIB$', desc[i])
            results.append([description, vals[i], now])
        return results
    except:
        print "SNMP ISSUES with %s using %s" % (host['DESC'], collector['DESC'])
        return "NoData"


def AddHostToQueue(host):
    """
    Adds host and collectors for host to queue
    """
    for collector in host["COLLECTORS"]:
        CollectorQueue.put([host, COLLECTORS[collector]])

def ProcessQueue():
    """
    Processes the collector queue
    """
    while not exitFlag:
        collector = CollectorQueue.get()
        if collector == None: break
        datums = Collector(collector[0], collector[1])
        for i in datums:
            graphitesender.GraphiteQueue.put(i)

def StartCollectorPool():
    if debug: print "Starting Collector Pool"
    for x in range(4):
        p = multiprocessing.Process(target = ProcessQueue)
        collectorpool.append(p)
        p.start()

def StopCollectorPool():
    for p in collectorpool:
        p.terminate()

