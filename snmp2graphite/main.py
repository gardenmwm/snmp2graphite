'''
Created on Jun 27, 2012

@author: garden

Main starting point for snmp2graphite, reads config files and starts everything
'''
import poller, graphitesender, scheduler, configurator

config = configurator.Config
#Setup  Graphite Variables
graphitesender.CARBON_PORT = int(config.GeneralOptions['CARBON_PORT'])
graphitesender.CARBON_SERVER = config.GeneralOptions['CARBON_SERVER']
debug=config.GeneralOptions['DEBUG']


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

