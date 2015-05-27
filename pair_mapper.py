#!/usr/bin/env python

import sys
from itertools import *
from ConfigParser import *

def init():
	"""
	This function initializes redis
	Returns: r_server (string): redis server init
	"""
	r_server = Redis('localhost')
	return r_server


config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    items = line.split(config.get('counting','delimiter'))
    for x in combinations(items,2):
        string = str(x[0]) + config.get('counting','delimiter') + str(x[1])
        print "%s%s%s"%(string,config.get('counting','separator'),1)
