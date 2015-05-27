#!/usr/bin/env python
"""
This code reduces input to generate all distinct items and their counts
"""

import sys
from ConfigParser import *
from redis import *
from math import *

def init():
	r_server = Redis('localhost')
	return r_server

def loop(items,r_server,count):
    cons = 0.0
    lst = items.split(config.get('counting','delimiter'))
    oc = r_server.hget('single',lst[0])
    try:
        oc1 = int(oc)
    except TypeError:
        return 0.0
    oc = r_server.hget('single',lst[1])
    try:
        oc2 = int(oc)
    except TypeError:
        return 0.0
    oc = count
    try:
        ocp = int(oc)
    except TypeError:
        return 0.0
    cons = ocp/sqrt(oc1*oc2)
    return cons

current_item = None
current_count = 0
item = None
config = ConfigParser()
config.read('config.ini')
r_server = init()
cons = 0.0
temp = []
for line in sys.stdin:
    line = line.strip()
    item,count = line.split(config.get('counting','separator'), 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if current_item:
        temp = current_item.split(config.get('counting','delimiter'))
    if current_item == item:
        current_count += count
    else:
        if current_item:
            temp = current_item.split(config.get('counting','delimiter'))
            try:
                if int(r_server.hget('single',str(temp[0]))) > int(config.get('denoising','single_threshold')) and int(r_server.hget('single',str(temp[1]))) > int(config.get('denoising','single_threshold')) and current_count > int(config.get('denoising','pair_threshold')):
                    cons = loop(current_item,r_server,current_count)
                    if cons > float(config.get('denoising','minimum_threshold')):
            	        print current_item + config.get('counting','separator') + str(cons)
                        r_server.hset('pair',current_item,cons)
            except TypeError:
                pass
        current_count = count
        current_item = item
if current_item == item:
    temp = current_item.split(config.get('counting','delimiter'))
    try:
        if int(r_server.hget('single',str(temp[0]))) > int(config.get('denoising','single_threshold')) and int(r_server.hget('single',str(temp[1]))) > int(config.get('denoising','single_threshold')):
            cons = loop(current_item,r_server,current_count)
            if cons > float(config.get('denoising','minimum_threshold')):
                print current_item + config.get('counting','separator') + str(cons)
                r_server.hset('pair',current_item,cons)
    except TypeError:
        pass
