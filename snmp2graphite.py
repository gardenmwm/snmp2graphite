'''
Created on Jun 27, 2012

@author: marsham
'''
import poller, graphitesender, configurator, scheduler

config = configurator.ReadConfig()
#Setup  Graphite Variables
graphitesender.CARBON_PORT = int(config[0]['CARBON_PORT'])
graphitesender.CARBON_SERVER = config[0]['CARBON_SERVER']

poller.StartCollectorPool()
graphitesender.StartGraphitePool()
HOSTS = config[1]
poller.COLLECTORS = config[2]
scheduler.makeschedules(HOSTS)

if __name__ == '__main__':

    for host in HOSTS:
        poller.AddHostToQueue(HOSTS[host])
    scheduler.ScheduleChecks(HOSTS)
    #for x in range(10):
    #    poller.CollectorQueue.put(None)
    for p in poller.collectorpool:
        p.join()
    #for x in range(10):
    #    graphitesender.GraphiteQueue.put(None)

