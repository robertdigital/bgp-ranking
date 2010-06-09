#!/usr/bin/python
import os 
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../../etc/bgp-ranking.conf")

temporary_dir = config.get('fetch_files','tmp_dir')
old_dir = config.get('fetch_files','old_dir')
sleep_timer = int(config.get('global','sleep_timer'))

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(root_dir,config.get('global','log_fetch_raw_files')))

import datetime 
import urllib
import filecmp
import glob
import time
    
"""
Fetch the raw file
"""

def usage():
    print "fetch_raw_files.py dir url"
    exit (1)

if len(sys.argv) < 2:
    usage()

args = sys.argv[1].split(' ')

temp_filename = os.path.join(args[0], temporary_dir, str(datetime.date.today()))
filename = os.path.join(args[0], str(datetime.date.today()))
old_directory = os.path.join(args[0], old_dir)

while 1:
    urllib.urlretrieve(args[1], temp_filename)
    drop_file = False
    to_check = glob.glob( os.path.join(old_directory, '*') )
    to_check += glob.glob( os.path.join(args[0], '*') )
    for file in to_check:
        if filecmp.cmp(temp_filename, file):
            drop_file = True
            break
    if drop_file:
        os.unlink(temp_filename)
        print('No new file on ' + args[1])
        logging.info('No new file on ' + args[1])
    else:
        os.rename(temp_filename, filename)
        print('New file on ' + args[1])
        logging.info('New file on ' + args[1])
    time.sleep(sleep_timer)