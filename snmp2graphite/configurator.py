'''
Created on Jun 27, 2012

@author: marsham
'''
import ConfigParser

def ReadConfig(configfile = 'config.ini'):
    parser = ConfigParser.SafeConfigParser()
    parser.read(configfile)
    GeneralOptions = {}
    Collectors = {}
    Hosts = {}
    for item in parser.options('General'):
        item = item.upper()
        GeneralOptions[item] = parser.get('General', item)
    #Parse out all hosts
    hostparser = ConfigParser.SafeConfigParser()
    hostparser.read(GeneralOptions['HOSTS'])
    for host in hostparser.sections():
        newhost = {}
        for item in hostparser.options(host):
            item = item.upper()
            newhost[item] = hostparser.get(host, item)
        newhost['COLLECTORS'] = newhost['COLLECTORS'].split(',')
        Hosts[host] = newhost

    #Parse out all Collectors
    collectorparser = ConfigParser.SafeConfigParser()
    collectorparser.read(GeneralOptions['COLLECTORS'])
    for collector in collectorparser.sections():
        newcollector = {}
        for item in collectorparser.options(collector):
            item = item.upper()
            newcollector[item] = collectorparser.get(collector, item)
        if newcollector['TYPE'] != 'table':
            newcollector['MIBDATA'] = (newcollector['MIBDATA']).split(',')
            newcollector['MIBDESC'] = (newcollector['MIBDESC']).split(',')
        if not newcollector.has_key('NAMING_SCHEMA'):
            newcollector['NAMING_SCHEMA'] = GeneralOptions['NAMING_SCHEMA']
        Collectors[collector] = newcollector
    return [GeneralOptions, Hosts, Collectors ]


class Config:
    def __init__(self, configdir="../config/"):
        self.GeneralOptions = {}
        self.Collectors = {}
        self.Hosts = {}
        self.__parseconfig__(configdir)

    def __parseconfig__(self,configdir):
        """
        Parse config files
        """
        # General Config Parser
        genparser = ConfigParser.SafeConfigParser()
        genparser.read(configdir + "config.ini")
        for item in genparser.options('General'):
            item = item.upper()
            self.GeneralOptions[item] = genparser.get('General', item)
        
        #Host Config Parser
        hostparser = ConfigParser.SafeConfigParser()
        hostparser.read(self.GeneralOptions['HOSTS'])
        for host in hostparser.sections():
            newhost = {}
            for item in hostparser.options(host):
                item = item.upper()
                newhost[item] = hostparser.get(host, item)
            newhost['COLLECTORS'] = newhost['COLLECTORS'].split(',')
            self.Hosts[host] = newhost
            
        #Collector Parser
        collectorparser = ConfigParser.SafeConfigParser()
        collectorparser.read(GeneralOptions['COLLECTORS'])
        for collector in collectorparser.sections():
            newcollector = {}
            for item in collectorparser.options(collector):
                item = item.upper()
                newcollector[item] = collectorparser.get(collector, item)
            if newcollector['TYPE'] != 'table':
                newcollector['MIBDATA'] = (newcollector['MIBDATA']).split(',')
                newcollector['MIBDESC'] = (newcollector['MIBDESC']).split(',')
            if not newcollector.has_key('NAMING_SCHEMA'):
                newcollector['NAMING_SCHEMA'] = self.GeneralOptions['NAMING_SCHEMA']
            self.Collectors[collector] = newcollector
        
            
