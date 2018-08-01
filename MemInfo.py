# -*- coding:utf-8 -*- 
# MemInfo.py
# Author: lishiyun(Swing Leo)
# Mail: lishiyun@163.com
# Created Time: Thu Aug 2 00:02:05 2017


from __future__ import print_function
from collections import OrderedDict

def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

if __name__=='__main__':
    meminfo = meminfo()
    print('Total memory: {0}'.format(meminfo['MemTotal']))
    print('Free memory: {0}'.format(meminfo['MemFree']))
