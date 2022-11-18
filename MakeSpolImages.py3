#!/usr/bin/python3

#=====================================================================
#
# Create images from SPOL data
#
#=====================================================================

from __future__ import print_function

import os
import sys
import time
import datetime
from datetime import timedelta
import glob
import shutil
import bz2

import string
import subprocess
from optparse import OptionParser

import urllib.request, urllib.parse, urllib.error
from xml.dom import minidom
from sys import stdin
from urllib.request import urlopen
from subprocess import call

def main():

    global options
    global tmpDir
    global startTime, endTime
    global archiveMode
    global fileCount

    # initialize file count

    fileCount = 0

    global thisScriptName
    thisScriptName = os.path.basename(__file__)

    # parse the command line

    parseArgs()
    
    # initialize
    
    beginString = "BEGIN: " + thisScriptName
    nowTime = datetime.datetime.now()
    beginString += " at " + str(nowTime)
    
    print("=============================================", file=sys.stderr)
    print(beginString, file=sys.stderr)
    print("=============================================", file=sys.stderr)

    # create dirs

    try:
        os.makedirs(options.imageDirBase)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: cannot make output dir: ", options.imageDirBase, file=sys.stderr)
            print("  ", exc, file=sys.stderr)

    try:
        os.makedirs(options.ncDirBase)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: cannot make output dir: ", options.ncDirBase, file=sys.stderr)
            print("  ", exc, file=sys.stderr)

    # realtime mode - loop forever

    if (options.realtimeMode):
        lookbackSecs = timedelta(0, int(options.lookbackSecs))
        while(True):
            fileCount = 0
            nowTime = time.gmtime()
            endTime = datetime.datetime(nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday,
                                        nowTime.tm_hour, nowTime.tm_min)
            startTime = endTime - lookbackSecs
            manageRetrieval(startTime, endTime)
            if (options.runOnce):
                break
            else:
                time.sleep(int(options.sleepSecs))
        return

    # archive mode - one shot

    manageRetrieval(startTime, endTime)
            
    endString = "END: " + thisScriptName
    nowTime = datetime.datetime.now()
    endString += " at " + str(nowTime)
    
    print("==============================================", file=sys.stderr)
    print(endString, file=sys.stderr)
    print("==============================================", file=sys.stderr)

    sys.exit(0)

########################################################################
# Manage the retrieval

def manageRetrieval(startTime, endTime):

    if (options.debug):
        print("Retrieving for times: ", 
              startTime, " to ", endTime, file=sys.stderr)

    if (startTime.day == endTime.day):

        # single day
        startDay = datetime.date(startTime.year, startTime.month, startTime.day)
        getForInterval(startDay, startTime, endTime)
        print("---->> Num files downloaded: ", fileCount, file=sys.stderr)
        return

    # multiple days

    tdiff = endTime - startTime
    tdiffSecs = tdiff.total_seconds()
    if (options.debug):
        print("Proc interval in secs:  ", tdiffSecs, file=sys.stderr)

    startDay = datetime.date(startTime.year, startTime.month, startTime.day)
    endDay = datetime.date(endTime.year, endTime.month, endTime.day)
    thisDay = startDay
    while (thisDay <= endDay):

        if (options.debug):
            print("===>>> processing day:  ", thisDay, file=sys.stderr)

        if (thisDay == startDay):
            # get to end of start day
            periodStart = startTime
            periodEnd = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                          23, 59, 59)
            getForInterval(thisDay, periodStart, periodEnd)

        elif (thisDay == endDay):
            # get from start of end day
            periodStart = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                            0, 0, 0)
            periodEnd = endTime
            getForInterval(thisDay, periodStart, periodEnd)

        else:
            # get for the full day
            periodStart = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                            0, 0, 0)
            periodEnd = datetime.datetime(thisDay.year, thisDay.month, thisDay.day,
                                          23, 59, 59)
            getForInterval(thisDay, periodStart, periodEnd)

        # go to next day
        thisDay = thisDay + timedelta(1)

    print("---->> Num files downloaded: ", fileCount, file=sys.stderr)

########################################################################
# Get the data for the specified time interval

def getForInterval(thisDay, startTime, endTime):

    thisDayStr = thisDay.strftime("%Y%m%d")
    dayDir = os.path.join(options.ncDirBase, thisDayStr)

    # get the local list of cfradial files

    localNcList = getLocalFileList(options.ncDirBase,thisDay)    

    for file in localNcList:

        # parse name and get dateTime string
        (junk,dateTime,junk,junk,junk) = file.split('.')
        dateTimeObj = datetime.datetime.strptime(dateTime,'%Y%m%d_%H%M%S')

        # create images if dateTimeObj in time window
        if dateTimeObj >= startTime and dateTimeObj <= endTime:
        
            if 'RHi1' in file or 'Rhi2' in file:
                outDirBase = options.imageDirBase+'/rhi'
                cmd = options.binDir+'/make_spol_rhi_plots.py3 '+dayDir+'/'+file+' '+outDirBase
                os.system(cmd)
            elif 'Sur1' in file or 'Sur2' in file:
                outDirBase = options.imageDirBase+'/ppi'
                cmd = options.binDir+'/make_spol_ppi_plots.py3 '+dayDir+'/'+file+' '+outDirBase
                if options.verbose:
                    print(cmd)
                os.system(cmd)
            elif 'User' in file:
                outDirBase = options.imageDirBase+'/rhi'
                cmd = options.binDir+'/make_spol_user_plots.py3 '+dayDir+'/'+file+' '+outDirBase
                os.system(cmd)
    
########################################################################
# Get list of files

def getLocalFileList(dirBase,date):

    # make the target directory and go there
    
    dateStr = date.strftime("%Y%m%d")
    dayDir = os.path.join(dirBase, dateStr)
    try:
        os.makedirs(dayDir)
    except OSError as exc:
        if (options.verbose):
            print("WARNING: trying to create dir: ", dayDir, file = sys.stderr)
            print("  exception: ", exc, file = sys.stderr)

    # get local file list - i.e. those which have already been downloaded
    
    os.chdir(dayDir)
    localFileList = os.listdir(dayDir)
    localFileList.reverse()

    if (options.verbose):
        print("==>> localFileList: ", localFileList, file=sys.stderr)

    return localFileList
            
########################################################################
# Parse the command line

def parseArgs():
    
    global options
    global startTime, endTime
    global archiveMode

    # parse the command line

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option('--debug',
                      dest='debug', default=False,
                      action="store_true",
                      help='Set debugging on')
    parser.add_option('--verbose',
                      dest='verbose', default=False,
                      action="store_true",
                      help='Set verbose debugging on')
    parser.add_option('--instance',
                      dest='instance',
                      default='test',
                      help='Provides uniqueness on the command line')
    parser.add_option('--ncDirBase',
                      dest='ncDirBase',
                      default='/tmp/aws',
                      help='Path of dir where the cfradial files are written')
    parser.add_option('--imageDirBase',
                      dest='imageDirBase',
                      default='/tmp/aws',
                      help='Path of dir to which the image files are written')
    parser.add_option('--binDir',
                      dest='binDir',
                      default='/tmp/bin',
                      help='Path of other scripts that are called')
    parser.add_option('--force',
                      dest='force', default=False,
                      action="store_true",
                      help='Force transfer even if file previously downloaded')
    parser.add_option('--dryRun',
                      dest='dryRun', default=False,
                      action="store_true",
                      help='Dry run: do not download data, list what would be downloaded')
    parser.add_option('--realtime',
                      dest='realtimeMode', default=False,
                      action="store_true",
                      help='Realtime mode - check every sleepSecs, look back lookbackSecs')
    parser.add_option('--runOnce',
                      dest='runOnce', default=False,
                      action="store_true",
                      help='Runs once for lookbackSecs and then exits')
    parser.add_option('--lookbackSecs',
                      dest='lookbackSecs',
                      default=1800,
                      help='Lookback secs in realtime mode')
    parser.add_option('--sleepSecs',
                      dest='sleepSecs',
                      default=10,
                      help='Sleep secs in realtime mode')
    parser.add_option('--start',
                      dest='startTime',
                      default='1970 01 01 00 00 00',
                      help='Start time for retrieval - archive mode')
    parser.add_option('--end',
                      dest='endTime',
                      default='1970 01 01 00 00 00',
                      help='End time for retrieval - archive mode')

    (options, args) = parser.parse_args()

    if (options.verbose):
        options.debug = True
        
    year, month, day, hour, minute, sec = options.startTime.split()
    startTime = datetime.datetime(int(year), int(month), int(day),
                                  int(hour), int(minute), int(sec))
    
    year, month, day, hour, minute, sec = options.endTime.split()
    endTime = datetime.datetime(int(year), int(month), int(day),
                                int(hour), int(minute), int(sec))
    if (startTime.year > 1970 and endTime.year > 1970):
        archiveMode = True
    else:
        archiveMode = False
    
    if (options.debug):
        print("Options:", file=sys.stderr)
        print("  debug? ", options.debug, file=sys.stderr)
        print("  verbose? ", options.verbose, file=sys.stderr)
        print("  instance ", options.instance, file=sys.stderr)
        print("  ncDirBase: ", options.ncDirBase, file=sys.stderr)
        print("  imageDirBase: ", options.imageDirBase, file=sys.stderr)
        print("  binDir: ", options.binDir, file=sys.stderr)
        print("  force? ", options.force, file=sys.stderr)
        print("  dryRun? ", options.dryRun, file=sys.stderr)
        print("  realtimeMode? ", options.realtimeMode, file=sys.stderr)
        print("  archiveMode? ", archiveMode, file=sys.stderr)
        print("  runOnce? ", options.runOnce, file=sys.stderr)
        print("  lookbackSecs: ", options.lookbackSecs, file=sys.stderr)
        print("  sleepSecs: ", options.sleepSecs, file=sys.stderr)
        print("  startTime: ", startTime, file=sys.stderr)
        print("  endTime: ", endTime, file=sys.stderr)

    if (options.realtimeMode == True and archiveMode == True):
        print("ERROR - ", thisScriptName, file=sys.stderr)
        print("  For realtime mode, do not set start or end times", file=sys.stderr)
        sys.exit(1)

########################################################################
# Run a command in a shell, wait for it to complete

def runCommand(cmd):

    if (options.debug):
        print("running cmd: ", cmd, file=sys.stderr)
    
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print("Child was terminated by signal: ", -retcode, file=sys.stderr)
        else:
            if (options.debug):
                print("Child returned code: ", retcode, file=sys.stderr)
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e

########################################################################
# kick off main method

if __name__ == "__main__":

   main()
