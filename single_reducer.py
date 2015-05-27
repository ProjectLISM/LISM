#!/usr/bin/env python
"""
This code reduces input to generate all distinct items and their counts
"""

import sys
from redis import *
from ConfigParser import *

def init():
	"""
	This function initializes redis
	Returns: r_server (string): redis server init
	"""
	r_server = Redis('localhost')
	return r_server

current_item = None
current_count = 0
item = None
r_server = init()
config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    print line
    item,count = line.split(config.get('counting','delimiter'), 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if current_item == item:
        current_count += count
    else:
        if current_item:
                r_server.hset("single",current_item,current_count)
        current_count = count
        current_item = item
if current_item == item:
    r_server.hset("single",current_item,current_count)
