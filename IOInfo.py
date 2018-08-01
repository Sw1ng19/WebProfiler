# -*- coding:utf-8 -*- 
# IOInfo.py
# Author: lishiyun(Swing Leo)
# Mail: lishiyun@163.com
# Created Time: Thu Aug 2 00:02:50 2017 

import time
import sys
 
if len(sys.argv) > 1:
    INTERFACE = sys.argv[1]
else:
    INTERFACE = 'eth0'
STATS = []
print 'Interface:',INTERFACE
 
def rx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in ifstat:
	if INTERFACE in interface:
	    stat = float(interface.split()[1])
	    STATS[0:] = [stat]
            
def tx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in ifstat:
	if INTERFACE in interface:
	    stat = float(interface.split()[9])
	    STATS[1:] = [stat]
            
if __name__ == "__main__":
    # print 'In & Out'
    # rx()
    # tx()
     
    while True:
        time.sleep(1)
        rxstat_o = list(STATS)
        rx()
        tx()
        RX = float(STATS[0])
        RX_O = rxstat_o[0]
        TX = float(STATS[1])
        TX_O = rxstat_o[1]
        RX_RATE = round((RX - RX_O)/1024/1024,3)
        TX_RATE = round((TX - TX_O)/1024/1024,3)
        print RX_RATE ,'MB',TX_RATE ,'MB'
