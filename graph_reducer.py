#!/usr/bin/env python
"""
This code reduces input to generate all distinct items and their counts
"""

import sys
from ConfigParser import *

current_node = None
current_item = None
item = None
node = None
config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    node,item = line.split(config.get('counting','separator'), 1)

    if current_node == node:
	if current_item == None:
		current_item = item
	else:
		current_item = current_item + config.get('counting','delimiter') + item
    else:
        if current_node:
            print current_node + config.get('counting','separator') + str(current_item)
        current_item = item
        current_node = node
if current_node == node:
    print current_node + config.get('counting','separator') + str(current_item)
