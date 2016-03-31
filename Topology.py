#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from mininet.node import Host
from mininet.node import Switch
import logging
import os
import commands
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )        
        
def shell(command):
    (status, output)=commands.getstatusoutput(command)
    log=open("shell_log.txt",'w')
    log.write(time.strftime('[%Y-%m-%d %H:%M:%S]\n',time.localtime(time.time())))
    log.write(output+'\n')
    return output #incase we need it.
    
def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()

def createTopo():

    logging.debug("Start Mininet")
    CONTROLLER_IP = "127.0.0.1"
    CONTROLLER_PORT = 6653
    net = Mininet(topo=None, link=TCLink, controller=None)
    net.addController( 'controller',controller=RemoteController,ip=CONTROLLER_IP,port=CONTROLLER_PORT)
    
    s1=net.addSwitch("s1")
    s2=net.addSwitch("s2")
    s3=net.addSwitch("s3")
    s4=net.addSwitch("s4")
    h1=net.addHost("h1",ip="0.0.0.0")
    h2=net.addHost("h2",ip="0.0.0.0")
    net.addLink(s1, h1, bw=100)
    net.addLink(s1, s2, bw=100)
    net.addLink(s1, s3, bw=100)
    net.addLink(s2, s4, bw=100)
    net.addLink(s3, s4, bw=100)
    net.addLink(h2, s1, bw=100)
    
    net.start()
    
    #shell commands:
    #connect hosts to the Internet
    shell("sudo ovs-vsctl add-port s4 eth1")
    h1.cmdPrint('dhclient -v')
    h2.cmdPrint('dhclient -v')
    #setup the sflow-rt agent
    shell("sudo ovs-vsctl add-port s1 eth0")
    shell("sudo ifconfig s1 10.0.0.106 netmask 255.255.255.248")
    shell("sudo ovs-vsctl -- --id=@sflow create sFlow agent=s1 target=\\\"127.0.0.1:6343\\\" "
          "header=128 sampling=64 polling=1 -- set bridge s1 sflow=@sflow")
    
    logger.debug("dumpNode")
    dumpNodeConnections(net.hosts)
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        createTopo()
