#!/usr/bin/env python
"""
This code gives all occurences of single items
"""
import sys
from ConfigParser import *
from redis import *

def init():
	"""
	This function initializes redis
	Returns: r_server (string): redis server init
	"""
	r_server = Redis('localhost')
	return r_server


def loop(items):
	"""
	This function loops each item and append count to one and prints it into file by hadoop.
	Args:
		items (List): It contains items filtered by filt()
	"""
	for item in items:
		print '%s%s%s' % (item,config.get('counting','delimiter'),1)

config = ConfigParser()
config.read('config.ini')
r_server = init()
r_server.delete('single')
for line in sys.stdin:
    line = line.strip()
    items = line.split(config.get('counting','delimiter'))
    loop(items)
