# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 14:37:02 2014

@author: Niel
"""
from os import path, listdir, remove
import pandas as pd
import datetime as dt
import calendar as cal
import logging
import sys

def last_month_end():
    td = dt.datetime.today()
    enddt = dt.date(td.year, td.month-1, cal.monthrange(td.year, td.month-1)[1])
    return(enddt)

def date_days_ago(days=0):
    td = dt.datetime.today()
    tmpd = td - dt.timedelta(days=days)

    return str(tmpd.date())


def getLog(name='root', filename=None):
    log = logging.getLogger(name)
    logFormatter = logging.Formatter("'%(asctime)s-%(name)s-[%(levelname)s] - %(message)s'")

    if filename == None:
        filename = name

    fileHandler = logging.FileHandler("{0}.log".format(filename))
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    log.addHandler(consoleHandler)

    return log

# helper functions    
def clear_tempfiles(root):
    '''
    
    '''
    print 'Looking in ' + root + '...'
    if listdir(root):
        # this folder contains files and sub directories
        for f in listdir(root):
            # for every file or sub directory in this directory 
        
            subpath = path.join(root, f)
            if path.isfile(subpath):
                # check if it is a file
                print 'Deleting file: ' + subpath
                # Delete file from directory
                remove(subpath)
            elif path.isdir(subpath):
                # else check if it is a directory
            
                # clear all files in directory and traverse subdirectories
                clear_tempfiles(subpath)
        