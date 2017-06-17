#! /usr/bin/env python3

import csv
import datetime
import time
import pprint
import json
import os

pp = pprint.PrettyPrinter(indent=4)
cycleDict={}
path="./sleepCharts/sleep-export.csv"

def sleepCSVreader(path):
    """Reads CSV File from Android as sleep
    Combines every two lines into a list of
    field,values pairs for each night
     for further parsing"""

    sleepList=[]
    with open(path) as sleepCsv:
        reader=csv.reader(sleepCsv)
        while reader:
            try:
                fields=(next(reader))
                values=(next(reader))
                sleepList.append(list(zip(fields,values)))
            except StopIteration:
                break
    return sleepList

def dictMaker(sleepEntry):
    """Takes a single nights entry,
    and returns a list of field,value pairs
    that can be added to dictionary
    """
    for i in range(13):
        tempList=[]
        if i in [4,8,9,10,]:
            pass


        elif i in [5,6,11,12]:
            key,value=sleepEntry[i]
            entryDict[key]=float(value)

        elif i in [0]:
            key,value=sleepEntry[i]
            entryDict[key]=int(value)

        else:
            key,value=sleepEntry[i]
            entryDict[key]=value

def phaseListMaker(sleepEntry):
    """Takes a single nights entry.
    Parses "Event" field, changes timestamp
    to date and time and returns list of
    pairs in format [time, sleepPhase]
    """
    phaseList=[]
    timeStampList=[]
    for item in sleepEntry:
        if 'Event' in item:
            if 'END' in item[1]:
                pass

            elif 'RR' in item[1]:
                pass

            else:
                pair=(item[1].split('-'))
                timestamp=(int(pair[1]))
                phaseTime = time.strftime('%m/%d %H:%M:%S',
                                            time.gmtime(timestamp/1000.))
                if ('EARLIEST' in pair[0] or
                    'LATEST' in pair[0] or
                    'BROKEN' in pair[0] or
                    'RR' in pair[0]):
                    pass
                elif 'ALARM' in pair[0]:
                     phase=pair[0]
                elif 'TRACKING' in pair[0]:
                    phase="TRACKING_STOPPED"
                else:
                    temp=pair[0].split('_')
                    phase=temp[0]
                phaseList.append([int(timestamp)/1000,phaseTime,phase])
                timeStampList.append(timestamp/1000)
    for i in range((len(timeStampList))-1):
        dur=(datetime.datetime.fromtimestamp(timeStampList[i+1]) -
                    datetime.datetime.fromtimestamp(timeStampList[i]))
        tempMins=(dur.seconds)/60.00
        durMins=("%.2f" % tempMins)
        phaseList[i].insert(2,float(durMins))
    phaseList[-1].insert(2,float(0.0))

    return phaseList

cycleData=[]
sleepList=sleepCSVreader(path)
for entry in sleepList:
    entryDict={}
    dictMaker(entry)
    phaseTimes=phaseListMaker(entry)
    entryDict['phases']=phaseTimes
    cycleData.append(entryDict)
cycleData.sort(key=lambda x: x['Id'])


pp.pprint(cycleData)
with open('./sleepCharts/sleep.json','w',encoding ='utf-8') as file:
    jsonCycles = json.dumps(cycleData)
    file.write(jsonCycles)
