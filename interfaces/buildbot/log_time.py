#!/usr/bin/python

import datetime, os

script_folder=os.path.split(os.path.realpath(__file__))[0]
file=open(os.path.join(script_folder, 'log.txt'), 'a')
file.write(str(datetime.datetime.now())+'\n')
