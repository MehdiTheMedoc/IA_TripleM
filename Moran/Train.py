import os
import time
import random
import sys
import getopt
import ntpath
import pickle

import MathHelper

import numpy as np

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor #futures
from concurrent.futures import as_completed

## Config
verbose = False
nbThread = 1

## Useful Variable
x = []
y = []
theta = []
alpha = 0.000005             # learning coef
n = 0                        # nb of data analyze
e = 0                        # nb of examples
trainTime = 1500             # nb of iteration on ALL examples

## Folder and Stuff
workingFolder = ''
fileName = ''
ext = ''
startTime = ''
saveFolder = ''
logsFileName = ''
outputFileName = ''
serializeFileName = ''

inputDataPath = ''
outputDataPath = ''
logsDataPath = ''
serializeDataPath = ''

## Nic'o-matic
hugeLine  = "================================================================="
hugeSpace = "                                                                 "

## Help' o-matic
def usage():
    print hugeSpace

    print "Many Help"
    print "Such IA"
    
    print hugeSpace

## Some function to replace multiple char by another in one call
def customReplace(string, olds, new=''):
    for old in olds:
        string.replace(old,new)
    return string

def readDataHandleLine(l):
    tmp = l.strip().split(',')
                
    y = float(tmp[0])
    x = [1 if i == 0 else float(tmp[i]) for i in range(len(tmp))]
    
    return x,y
    
## Read the dataFile given and return e, n, x, y with X threads
def readDataThread(nbThread):
    global inputDataPath

    print "Debug : reading file (threaded Mode)"
    print "Reading from " + inputDataPath
    
    f = open(inputDataPath, "r+")
    
    x = []
    y = []
    lineCount = 0
    
    with open(inputDataPath, "r") as tmpf:
        lineCount = sum(bl.count("\n") for bl in blocks(tmpf))
            
        
     
    # res = multiprocessing(readDataHandleLine, [line for line in f], nbThread)
    
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=nbThread) as executor:
        jobs = {}

        lines_left = lineCount

        MAX_JOBS_IN_QUEUE = 8
        
        while lines_left:
        
            if lineCount%10000 == 0:
                print still 
        
            for line in f:
                job = executor.submit(readDataHandleLine, line)
                jobs[job] = line
                if len(jobs) > MAX_JOBS_IN_QUEUE:
                    break

            for job in as_completed(jobs):
                lines_left -= 1

                results_list = job.result()

                del jobs[job]

                x.append(results_list[0])
                y.append(results_list[1])
    
                break;
                
    print "ThreadPoolExecutor : %ds" % (time.time()-start)
    
    print "Debug : reading done"
    
    dataCount = len(x[0])
    
    return lineCount, dataCount, x, y
    
## Read the dataFile given and return e, n, x, y
def readData():
    print "Debug : reading file"
    print "Reading from " + inputDataPath
    
    f = open(inputDataPath, 'r+')

    x = []
    y = []
    lineCount = 0

    for line in f:
        lineCount+=1
        tmp = line.strip().split(',')
                
        y.append(float(tmp[0]))
        x.append( [1 if i == 0 else float(tmp[i]) for i in range(len(tmp))] )

        if lineCount%10000 == 0:
            print lineCount

    f.close

    dataCount = len(x[0])

    print "Debug : reading done"
    
    return lineCount, dataCount, x, y

## Save what has been done do use it later
def save(theta):
    # f = open(filename, 'r+')

    f.write(str(i))
    f.close
    
## Test serialize/unserialize
def serialize():
    global x, y, n, e
    
    print "Serializing data"
    start = time.time()
    serializeData = {}
    serializeData['x'] = x
    serializeData['y'] = y
    serializeData['n'] = n
    serializeData['e'] = e
    with open(serializeDataPath, 'wb') as f:
        pickle.dump(serializeData, f)
    end = time.time()
    print "Serializing data done in (%ss)" % (end - start)
    
    print "Unserializing data"
    start = time.time()
    with open(serializeDataPath, 'rb') as f:
        unserializeData = pickle.load(f)
    end = time.time()
    print "Unserializing data done in (%ss)" % (end - start)
    
## Get the data
def getData(useThread = True):
    global x, y, theta, alpha, n, e, trainTime
    
    start = time.time()
    if useThread:        
        e,n,x,y = readDataThread(8)
    else:
        e,n,x,y = readData()
    end = time.time()

    print "Using Threads : %r : %ds" % (useThread, end - start)
    
## Train the model with some fancy magic of gradient
def train(useThread = True):
    global x, y, theta, alpha, n, e, trainTime
    
    start = time.time()
    
    theta = [ 0 for i in range(n)]

    print "Debug : training..."

    # training theta
    for train in range(trainTime): #redo the train trainTime times
        if (train%200) == 0:
            print "train number %d/%d" % (train, trainTime)
            print theta
        for i in range(e): #each example => to put in some thread, each thread do some example
            
            if useThread:

                print "not implemented !!"
            
            else:
                for j in range(n): #each data type => to put in n thread, each thread do one theta

                    # update the corresponding theta
                    sumDerivated = 0

                    for t in range(e):
                        sumDerivated += (MathHelper.arrayProduct(theta, x[t]) - y[t]) * x[t][j]
                
                    theta[j] -= alpha * ( float(1) / e ) * sumDerivated
                    # if (j % 10 ) == 0:
                        # print "%s/%s" % (j,n)
            # print theta
            # print MathHelper.arrayProduct(theta, [1,49.94357,21.47114,73.07750,8.74861,-17.40628,-13.09905,-25.01202,-12.23257,7.83089,-2.46783,3.32136,-2.31521,10.20556,611.10913,951.08960,698.11428,408.98485,383.70912,326.51512,238.11327,251.42414,187.17351,100.42652,179.19498,-8.41558,-317.87038,95.86266,48.10259,-95.66303,-18.06215,1.96984,34.42438,11.72670,1.36790,7.79444,-0.36994,-133.67852,-83.26165,-37.29765,73.04667,-37.36684,-3.13853,-24.21531,-13.23066,15.93809,-18.60478,82.15479,240.57980,-10.29407,31.58431,-25.38187,-3.90772,13.29258,41.55060,-7.26272,-21.00863,105.50848,64.29856,26.08481,-44.59110,-8.30657,7.93706,-10.73660,-95.44766,-82.03307,-35.59194,4.69525,70.95626,28.09139,6.02015,-37.13767,-41.12450,-8.40816,7.19877,-8.60176,-5.90857,-12.32437,14.68734,-54.32125,40.14786,13.01620,-54.40548,58.99367,15.37344,1.11144,-23.08793,68.40795,-1.82223,-27.46348,2.26327])
    
    end = time.time()

    print "Debug : training done, Using Threads : %r in %ds" % (useThread, end - start)

    print "=========================================="
    
    print "Debug : testing..."
    
    if n > 5:
        print "Congratz, you waited so long, you should be dead long ago :3 (2001 by the way ^^)"
        print MathHelper.arrayProduct(theta, [1,49.94357,21.47114,73.07750,8.74861,-17.40628,-13.09905,-25.01202,-12.23257,7.83089,-2.46783,3.32136,-2.31521,10.20556,611.10913,951.08960,698.11428,408.98485,383.70912,326.51512,238.11327,251.42414,187.17351,100.42652,179.19498,-8.41558,-317.87038,95.86266,48.10259,-95.66303,-18.06215,1.96984,34.42438,11.72670,1.36790,7.79444,-0.36994,-133.67852,-83.26165,-37.29765,73.04667,-37.36684,-3.13853,-24.21531,-13.23066,15.93809,-18.60478,82.15479,240.57980,-10.29407,31.58431,-25.38187,-3.90772,13.29258,41.55060,-7.26272,-21.00863,105.50848,64.29856,26.08481,-44.59110,-8.30657,7.93706,-10.73660,-95.44766,-82.03307,-35.59194,4.69525,70.95626,28.09139,6.02015,-37.13767,-41.12450,-8.40816,7.19877,-8.60176,-5.90857,-12.32437,14.68734,-54.32125,40.14786,13.01620,-54.40548,58.99367,15.37344,1.11144,-23.08793,68.40795,-1.82223,-27.46348,2.26327])
    else:
        print "testing for 626, should be 1565"
        print MathHelper.arrayProduct(theta, [1, 626,626])
    
    print "Debug : many wow!"

    #raw_input('Press Start \r\n')
    # sys.exit("Bye !!")

def makeFolder():
    ## Normalize input
    global inputDataPath, workingFolder, fileName, fileName, ext, startTime
    global saveFolder, logsFileName, outputFileName, serializeFileName
    global outputDataPath, logsDataPath, serializeDataPath
    
    inputDataPath = ntpath.normcase(inputDataPath)

    ## Folder/File/Ext Names
    workingFolder, fileName = ntpath.split(inputDataPath)
    fileName, ext = ntpath.splitext(fileName)
    # startTime = time.strftime("%x_%X") <= probleme sur win avec : dans le nom de fichier
    startTime = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
    saveFolder = ntpath.join(workingFolder, fileName) + "Results"
    logsFileName = startTime + "_Logs"
    outputFileName = startTime + "_Load"
    serializeFileName = startTime + "_Serialize"
    
    outputDataPath = ntpath.join(saveFolder, logsFileName)
    logsDataPath = ntpath.join(saveFolder, outputFileName)
    serializeDataPath = ntpath.join(saveFolder, serializeFileName)
            
    ## Make dir
    if not ntpath.isdir(saveFolder):
        os.makedirs(saveFolder)

    a = open(outputDataPath, 'w+')
    a = open(logsDataPath, 'w+')

# https://stackoverflow.com/questions/9629179/python-counting-lines-in-a-huge-10gb-file-as-fast-as-possible
# with open("fileName", "r") as f:
    # print sum(bl.count("\n") for bl in blocks(f))
def blocks(f, size=65536):
    while True:
        b = f.read(size)
        if not b: 
            break
        yield b
        
def multiprocessing(func, args, workers):
    with ProcessPoolExecutor() as executor:
        res = executor.map(func, args)
    return list(res)
    
    
def multithreading(func, args, workers):
    with ThreadPoolExecutor() as executor:
        res = executor.map(func, args)
    return list(res)
    
## Progress Bar
def printProgressBar (i, max, prefix = "", suffix = "", doneChar = 'X', toDoChar = '_'):
    lenghtInChar = 65 - 8 - len(prefix) - len(suffix)
    print '\r%s [%s] %s%% %s\r' % (prefix, ''.join( [doneChar]*(lenghtInChar*i/max) + [toDoChar]*(lenghtInChar-lenghtInChar*i/max) ), int(10000 * ( float(i)/max )) / 100.0, suffix),

    if i == max:
        print ""
    
## Main
if __name__ == "__main__":
    
    try:
        os.system('clear')
    except:
        print hugeLine
    else:
        os.system('cls')
    
    print hugeSpace
    print " _____  ___   ______ _____ _____ _____  ______ _____ _   ___   __"
    print "|_   _|/ _ \  | ___ \  ___/  ___|_   _| | ___ \  _  | \ | \ \ / /"
    print "  | | / /_\ \ | |_/ / |__ \ `--.  | |   | |_/ / | | |  \| |\ V / "
    print "  | | |  _  | | ___ \  __| `--. \ | |   |  __/| | | | . ` | \ /  "
    print " _| |_| | | | | |_/ / |___/\__/ / | |   | |   \ \_/ / |\  | | |  "
    print " \___/\_| |_/ \____/\____/\____/  \_/   \_|    \___/\_| \_/ \_/  "
    print hugeSpace
    
    loadTime = 5000
    for i in range(loadTime):
        printProgressBar(i,loadTime-1, "Loading")
    
    print hugeSpace
    print hugeLine
    print hugeSpace
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["help", "input=", "verbose"])
    except getopt.GetoptError as err:
        ## Error in arguments
        print str(err)
        usage()
        sys.exit(2)

    ## Mandatory 
    inputDataPathFound = False

    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-i", "--input"):
            inputDataPath = a
            inputDataPathFound = True
        else:
            assert False, "Unhandled Option !"
                
    ## Mandatory Check      
    if not inputDataPathFound: ## Is an input given?
        print "Error : -i [file_path] or --input [file_path] was not given"
        usage()
        sys.exit(2)

    if not ntpath.isfile(inputDataPath): ## Is input a file?
        print "The path given as an input is not a file"
        usage()
        sys.exit(2)
    
    makeFolder()
    getData(True)
    # getData(False)
    # train(False)
    # train()