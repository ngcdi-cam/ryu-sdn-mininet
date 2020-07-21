#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 10:26:46 2019

@author: mep53
"""

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet_rest import MininetRest
from mininet.topo import LinearTopo
from mininet.topo import SingleSwitchTopo
from mininet.topolib import TreeTopo
from functools import partial
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log  import setLogLevel, info
import logging
import time
import threading
import sys
import subprocess 
from datetime import datetime
#LOG = logging.getLogger(os.path.basename(__file__))

#LOG = logging.getLogger(__name__)
setLogLevel('info')

def thread_launch(net):
    mininet_rest = MininetRest(net)
    mininet_rest.run(host='0.0.0.0', port=9081)

def thread_traffic(net,host_src,host_target_ip, bandw):
    time.sleep(20)
    info("About to trigger traffic")
#    net.hosts[host_src].sendCmd("iperf -u -t 6000 -c " + host_target_ip + " -b 80M")
    net.hosts[host_src].sendCmd("iperf -u -t 90 -c " + host_target_ip + " -b " + bandw )
    info("Triggered Iperf "+ str(host_src) +" -> "+host_target_ip)
    
def thread_failure(net):
    info("Wait for failure")
    #time.sleep(240)
    time.sleep(10)
    info("Failure to trigger")
    #switch.sendCmd("ifconfig s1-eth0 down")
    #net.switches[4].cmd("ifconfig s5-eth1 down")
    #net.switches[4].cmd("ifconfig s4-eth2 down")
    info("Failure triggered\n")
    #time.sleep(20)
    #net.hosts[7].cmd("iperf -u -t 580 -c 10.0.0.2 -b 500M ") #150
    info("new traffic triggered\n")
    
#    net.switches[4].cmd("ifconfig s4-eth3 down")

def thread_console(net):
    #net.hosts[8].sendCmd("iperf -u -t 600 -c 10.0.0.1 -b 500000000")
    CLI(net)

def thread_t1(net):
    #net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 28M ")
    #info("triggered traffic 1\n")
    #net.hosts[9].cmd("iperf -u -t 40 -c 10.0.0.1 -b 42M ")
    #info("triggered traffic 2\n")
    #net.hosts[9].cmd("iperf -u -t 20 -c 10.0.0.1 -b 130M ")
    #info("triggered traffic 3\n")
    #net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 70M ")
    #info("triggered traffic 4\n")
    #net.hosts[9].cmd("iperf -u -t 60 -c 10.0.0.1 -b 500M ")
    #info("triggered traffic 5\n")
    #net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 30M ")
    #info("triggered traffic 6\n")
    #net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 200M ")
    #info("triggered traffic 7\n")
    info("[%s] h10 to h1 : starting traffic 1\n", datetime.now())
    net.hosts[9].cmd("iperf -u -t 160 -c 10.0.0.1 -b 300M ")
    info("[%s] h10 to h1 : ended traffic 1, starting traffic 2\n",datetime.now())
 #   time.sleep(65)
    net.hosts[9].cmd("iperf -u -t 360 -c 10.0.0.1 -b 800M ")
    info("[%s] h10 to h1 : ended traffic 2\n",datetime.now())

def thread_t2(net):
    info("h6 to h2 : starting traffic 1\n")
#
    net.hosts[6].cmd("iperf -u -t 240 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 1, starting failure\n",datetime.now())
    net.switches[4].cmd("ifconfig s4-eth2 down")
    info("[%s] h7 to h2 : ended failure, starting traffic 2\n",datetime.now())
    net.hosts[6].cmd("iperf -u -t 30 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 2\n",datetime.now())
    net.hosts[6].cmd("iperf -u -t 30 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 3\n",datetime.now())
    net.hosts[6].cmd("iperf -u -t 30 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 4\n",datetime.now())
    net.hosts[6].cmd("iperf -u -t 30 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 5\n",datetime.now())
    net.hosts[6].cmd("iperf -u -t 500 -c 10.0.0.2 -b 500M ") #150
    info("[%s] h7 to h2 : ended traffic 6\n",datetime.now())
#    time.sleep(105)
   # net.hosts[6].cmd("iperf -u -t 300 -c 10.0.0.7 -b 400M ")
   # info("h6 to h2 : ended traffic 2\n")




class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

c1 = RemoteController('c1', ip=sys.argv[1], port=6633)


cmap = { 's0': c1,'s1': c1, 's2': c1, 's3':c1, 's4':c1,  's5': c1, 's6': c1, 's7':c1, 's8':c1,  's9': c1, 's10': c1 }
#cmap = { 's1': c1}


net = Mininet(topo=None, cleanup=True, link=TCLink, autoSetMacs=True, switch=MultiSwitch, build=False )

for c in [ c1 ]:
    net.addController(c)

hosts = []

for i in range(1,11):
    hosts.append(net.addHost('h'+str(i)))

switches = []
for j in range(1,11):
    switches.append(net.addSwitch('s'+str(j)))


#inner ring
net.addLink(switches[0], switches[1], 1,1)
net.addLink(switches[1], switches[2], 2,1)
net.addLink(switches[2], switches[3], 2,1)
net.addLink(switches[3], switches[4], 2,1)
net.addLink(switches[4], switches[0], 2,2)

#outer switches
net.addLink(switches[0], switches[5], 3,1)
net.addLink(switches[1], switches[6], 3,1)
net.addLink(switches[2], switches[7], 3,1)
net.addLink(switches[3], switches[8], 3,1)
net.addLink(switches[4], switches[9], 3,1)


#hosts
net.addLink(switches[5], hosts[0], 2)
net.addLink(switches[5], hosts[1], 3)
net.addLink(switches[6], hosts[2], 2)
net.addLink(switches[6], hosts[3], 3)
net.addLink(switches[7], hosts[4], 2)
net.addLink(switches[7], hosts[5], 3)

net.addLink(switches[8], hosts[6], 2)
net.addLink(switches[8], hosts[7], 3)

net.addLink(switches[9], hosts[8], 2)
net.addLink(switches[9], hosts[9], 3)

#net.addLink(switches[10], hosts[9], 2)
#net.addLink(switches[10], hosts[10], 3)


info( '*** StartING network\n')
net.build()
net.start()

#tl = threading.Thread(target=thread_launch,args=(net, ))
#tl.start()
#info("Started network\n")

#tt1 = threading.Thread(target=thread_traffic,args=(net,8,'10.0.0.1', ))
#tt1 = threading.Thread(target=thread_traffic,args=(net,9,'10.0.0.1', '67M', ))
#tt2 = threading.Thread(target=thread_traffic,args=(net,9,'10.0.0.1', '42M', ))
#tl.join()
#tt2.start()
#tt1.start()
#time.sleep(30)

#net.dumpNodeConnections( net.nodelist )

#for node in net.nodeList:
theLinks = []
for node in net.items():
    info( '%s\n' % repr( node[1] ) )

info('\n----------------\n')

for lk in net.links: #linksBetween(switches[9],hosts[8])
    #info('%s\n' % repr(lk.intf1))
    info(lk.intf1.name+'<->'+lk.intf2.name+' '+lk.status()+"\n")
    info(lk.intf1.name+ ' ['+lk.intf1.mac+']<->'+lk.intf2.name+ '['+lk.intf2.mac+']\n')
    
t1 = threading.Thread(target=thread_t1,args=(net, ))
info(" t1 created\n")

t2 = threading.Thread(target=thread_t2,args=(net, ))
info(" t2 created\n")

t2.start()
info(" t2 started\n")

t1.start()
info(" t1 started\n")

tf = threading.Thread(target=thread_failure,args=(net, ))
tf.start()
info(" t failure started\n")

tf.join()
info(" tf joined\n")

info('-------------------\n')
for lk in net.links: #linksBetween(switches[9],hosts[8])
    info(lk.intf1.name+'<->'+lk.intf2.name+' '+lk.status()+"\n")

t2.join()
info(" t2 joined\n")

t1.join()
info(" t1 joined\n")
#time.sleep(10)


#net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 28M ")
#info("triggered traffic 1\n")
#net.hosts[9].cmd("iperf -u -t 40 -c 10.0.0.1 -b 42M ")
#info("triggered traffic 2\n")
#net.hosts[9].cmd("iperf -u -t 20 -c 10.0.0.1 -b 130M ")
#info("triggered traffic 3\n")
#net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 70M ")
#info("triggered traffic 4\n")
#net.hosts[9].cmd("iperf -u -t 60 -c 10.0.0.1 -b 500M ")
#info("triggered traffic 5\n")
#net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 30M ")
#info("triggered traffic 6\n")
#net.hosts[9].cmd("iperf -u -t 30 -c 10.0.0.1 -b 200M ")
#info("triggered traffic 7\n")

#tt2.start()
#net.hosts[9].sendCmd("iperf -u -t 90 -c 10.0.0.1 -b 30M ")
#info("triggered traffic 2\n")

#tf = threading.Thread(target=thread_failure,args=(net, ))
#tf.start()
#info("triggered failure")

# tc = threading.Thread(target=thread_console,args=(net, ))
# tc.start()
# info("Triggered Terminal")

#tl.join()
#tt1.join()

#tt1.join()
#info("Completed 1 joins")
#tt2.join()
#tl.join()
#tf.join()
#tc.join()
#info("Completed 2 joins")
#time.sleep(240)
net.stop()
