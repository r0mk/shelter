#!/usr/bin/python3

import os
import re

filename="/home/r0mk/log"

def method_1(filename):
    """Method 1: read whole file and regex"""
    regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(filename, 'r') as f:
        txt = f.read()
    match = re.findall(regex, txt)
    if match:
        #print(match.group())
        print(match)

