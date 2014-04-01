'''
Created on Jun 27, 2012

@author: marsham
'''
from socket import socket
import sys
from multiprocessing import Queue
import multiprocessing

GraphiteQueue = Queue()
exitFlag = 0
graphitesenderpool = []
#debug = 0
CARBON_SERVER = "127.0.0.1"
CARBON_PORT = 2003
CARBONSOCKET = socket()


def SendToGraphite(datum):
    """
    Sends data to graphite
    Datum is [Name,Value,Time]
    """
    if debug: print "SendToGraphite %s" % (datum)
    if datum != "NoData":
        try:
		GraphiteString = datum[0] + " " + datum[1] + " " + str(datum[2]) + "\n"
        	CARBONSOCKET.sendall(GraphiteString)
	except:
		print "Error sending data for ",
		print datum


def ProcessGraphiteQueue():
    while not exitFlag:
        datum = GraphiteQueue.get()
        if debug: print "Process Graphite Queue item %s" % (datum)
        #if datum == None: break
        SendToGraphite(datum)

def StartGraphitePool():
    if debug: print "STarting graphite pool"
    try:
        CARBONSOCKET.connect((CARBON_SERVER, CARBON_PORT))
    except:
            print "Bailing"
            sys.exit(1)
    for x in range(2):
        if debug: print "Starting graphite process queue"
        p = multiprocessing.Process(target = ProcessGraphiteQueue)
        graphitesenderpool.append(p)
        p.start()

