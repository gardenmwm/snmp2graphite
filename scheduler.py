import sched
import poller
import time

SCHEDULES = {}
SCHEDULER = sched.scheduler(time.time, time.sleep)
debug=1

def makeschedules(hosts):
    if debug: print "Making Schedules"
    for host, hostdef in hosts.iteritems():
        if SCHEDULES.has_key(hostdef['CHECKINTERVAL']):
            SCHEDULES[hostdef['CHECKINTERVAL']].append(host)
        else:
            SCHEDULES[hostdef['CHECKINTERVAL']] = [host]

def AddToQueue(host,schedule,HOSTS,scheduler):
    if debug: print "Adding to queue"
    #scheduler=sched.scheduler(time.time, time.sleep)
    scheduler.enter(int(schedule) * 60, 1, AddToQueue, (host, schedule, HOSTS, scheduler))
    poller.AddHostToQueue(HOSTS[host])

def ScheduleChecks(HOSTS):
    if debug: print "Scheduleing Checks"
    for schedule, hosts in SCHEDULES.iteritems():
        for host in hosts:
            if debug: print "Scheduling for %s in %s" % (host,schedule)
            SCHEDULER.enter(int(schedule) * 60, 1, AddToQueue, (host, schedule, HOSTS, SCHEDULER))
    SCHEDULER.run()

