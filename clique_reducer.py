#!/usr/bin/env python

import sys
from ConfigParser import *

def intersection(current_item,item):
    if current_item == '':
        return ''
    current_item = current_item.strip()
    a = current_item.split(config.get('counting','delimiter'))
    if item == '':
        return ''
    item = item.strip()
    b = item.split(config.get('counting','delimiter'))
    c = ''
    for i in range(0,len(a)):
        if a[i] in b:
            if c == '':
                c = a[i]
            else:
                c = c + config.get('counting','delimiter') + a[i]
    return c

current_node = None
current_item = 0
node = None
config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    try:
        node,item = line.split(config.get('counting','separator'), 1)
    except ValueError:
        node = line
        item = ''
    if current_node == node:
        current_item  = intersection(current_item,item)
    else:
        if current_node:
                print current_node + config.get('counting','separator') + str(current_item)
        current_item = item
        current_node = node
if current_node == node:
    current_item = intersection(current_item,item)
    print current_node + config.get('counting','separator') + str(current_item)
