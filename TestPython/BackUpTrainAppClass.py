import os, time, random, sys, getopt, ntpath

import MathHelper

import threading
import Queue

class ReadingThreadClass(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.partialX = []
        self.partialY = []
        
    def run(self):
        print "Starting " + self.name
        while not readExitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                
                tmp = data.strip().split(',')
                    
                self.partialX.append(float(tmp[0]))
                self.partialY.append( [1 if i == 0 else float(tmp[i]) for i in range(len(tmp))] )
            else:
                queueLock.release()
            # time.sleep(1)
        print "Exiting " + self.name

class App:

    ## Threads Related Variables
    globalThreadID = 1
    #### Read Threads
    readExitFlag = 0
    readQueue = Queue.Queue()
    readThreads = []
    readQueueLock = threading.Lock()

    ## Config
    verbose = False
    nbThread = 1
    
    ## Useful Variable
    x = []
    y = []
    tetha = []
    alpha = 0.000005            # learning coef
    n = 0                        # nb of data analyze
    e = 0                        # nb of examples
    trainTime = 1                # nb of iteration on ALL examples
    
    ## Folder and Stuff
    workingFolder = ''
    fileName = ''
    ext = ''
    startTime = ''
    saveFolder = ''
    logsFile = ''
    outputFile = ''
    
    inputDataPath = ''
    outputDataPath = ''
    logDataPath = ''
    
    ## Debug Every Variables
    def debugAll(self):
        print 'verbose          ' + str(self.verbose)
        print 'nbThread         ' + str(self.nbThread)
        print 'x                ' + str(self.x)
        print 'y                ' + str(self.y)
        print 'tetha            ' + str(self.tetha)
        print 'alpha            ' + str(self.alpha)
        print 'n                ' + str(self.n)
        print 'e                ' + str(self.e)
        print 'trainTime        ' + str(self.trainTime)
        print 'workingFolder    ' + str(self.workingFolder)
        print 'fileName         ' + str(self.fileName)
        print 'ext              ' + str(self.ext)
        print 'startTime        ' + str(self.startTime)
        print 'saveFolder       ' + str(self.saveFolder)
        print 'logsFile         ' + str(self.logsFile)
        print 'outputFile       ' + str(self.outputFile)
        print 'inputDataPath    ' + str(self.inputDataPath)
        print 'outputDataPath   ' + str(self.outputDataPath)
        print 'logDataPath      ' + str(self.logDataPath)

    ## Help' o-matic
    def usage(self):
        print "toDo Usage()"

    ## Some function to replace multiple char by another in one call
    def customReplace(self, string, olds, new=''):
        for old in olds:
            string.replace(old,new)
        return string

    ## Read the dataFile given and return e, n, x, y with X threads
    def readDataThread(self, nbThread):
        print "Debug : reading file (threaded Mode)"
        print "Reading from " + self.inputDataPath
        
        threadList = ["ReadingThread-%i" % (i) for i in range(nbThread)]
        
        # Create new threads
        for tName in threadList:
            thread = ReadingThreadClass(self.globalThreadID, tName)
            thread.start()
            self.readThreads.append(thread)
            self.globalThreadID += 1

        # Fill the queue
        f = open(self.inputDataPath, 'r+')
        
        self.readQueueLock.acquire()

        for line in f:
            self.readQueue.put(line)
            
        self.readQueueLock.release()

        # Wait for queue to empty
        while not self.readQueue.empty():
            pass

        # Notify threads it's time to exit
        self.readExitFlag = 1

        # Wait for all threads to complete
        for t in self.readThreads:
            t.join()
            for e in t.partialX:
                print e
            
        print "Debug : reading done"
        
        return lineCount, dataCount, x, y
        
        
        
    ## Read the dataFile given and return e, n, x, y
    def readData(self):
        print "Debug : reading file"
        print "Reading from " + self.inputDataPath
        
        f = open(self.inputDataPath, 'r+')

        x = []
        y = []
        lineCount = 0

        for line in f:
            lineCount+=1
            tmp = line.strip().split(',')
                    
            y.append(float(tmp[0]))
            x.append( [1 if i == 0 else float(tmp[i]) for i in range(len(tmp))] )

            if verbose:
                print "reading " + str(lineCount)

        f.close

        dataCount = len(x[0])

        print "Debug : reading done"
        
        return lineCount, dataCount, x, y

    ## Save what has been done do use it later
    def save(self, theta, filename):
        f = open(filename, 'r+')

        f.write(str(i))
        f.close
        
    ## Train the model with some fancy magic of gradient
    def train(self, dataFile):
        # self.e,self.n,self.x,self.y = self.readData()
        self.e,self.n,self.x,self.y = self.readDataThread(25)
        
        self.theta = [ 0 for i in range(n)]
        print self.theta

        print "Debug : training..."
        
        # training theta
        for time in range(50): #redo the train x times
            for i in range(self.e): #each example
                for j in range(self.n): #each data type

                    # update the corresponding theta
                    sumDerivated = 0

                    for t in range(self.e):
                        sumDerivated += (MathHelper.arrayProduct(self.theta, self.x[t]) - self.y[t]) * self.x[t][j]
                
                    self.theta[j] -= self.alpha * ( float(1) / self.e ) * sumDerivated

            print self.theta
            
        print "Debug : training done!"


        print "Debug : testing..."
        
        # print MathHelper.arrayProduct(theta, [1,49.94357,21.47114,73.07750,8.74861,-17.40628,-13.09905,-25.01202,-12.23257,7.83089,-2.46783,3.32136,-2.31521,10.20556,611.10913,951.08960,698.11428,408.98485,383.70912,326.51512,238.11327,251.42414,187.17351,100.42652,179.19498,-8.41558,-317.87038,95.86266,48.10259,-95.66303,-18.06215,1.96984,34.42438,11.72670,1.36790,7.79444,-0.36994,-133.67852,-83.26165,-37.29765,73.04667,-37.36684,-3.13853,-24.21531,-13.23066,15.93809,-18.60478,82.15479,240.57980,-10.29407,31.58431,-25.38187,-3.90772,13.29258,41.55060,-7.26272,-21.00863,105.50848,64.29856,26.08481,-44.59110,-8.30657,7.93706,-10.73660,-95.44766,-82.03307,-35.59194,4.69525,70.95626,28.09139,6.02015,-37.13767,-41.12450,-8.40816,7.19877,-8.60176,-5.90857,-12.32437,14.68734,-54.32125,40.14786,13.01620,-54.40548,58.99367,15.37344,1.11144,-23.08793,68.40795,-1.82223,-27.46348,2.26327])
        print MathHelper.arrayProduct(theta, [1, 626,626])
        
        print "Debug : many wow!"

        #raw_input('Press Start \r\n')
        sys.exit("Bye !!")

    def makeFolder(self):
        ## Normalize input
        self.inputDataPath = ntpath.normcase(self.inputDataPath)
    
        ## Folder/File/Ext Names
        self.workingFolder, self.fileName = ntpath.split(self.inputDataPath)
        self.fileName, self.ext = ntpath.splitext(self.fileName)
        # self.startTime = time.strftime("%x_%X") <= probleme sur win avec : dans le nom de fichier
        self.startTime = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        self.saveFolder = ntpath.join(self.workingFolder, self.fileName) + "Results"
        self.logsFile = self.startTime + "_Logs"
        self.outputFile = self.startTime + "_Load"
        
        self.outputDataPath = ntpath.join(self.saveFolder, self.logsFile)
        self.logDataPath = ntpath.join(self.saveFolder, self.outputFile)
                
        ## Make dir
        if not ntpath.isdir(self.saveFolder):
            os.makedirs(self.saveFolder)

        test = open(self.outputDataPath, 'w+')

        self.debugAll()
        self.train(self.inputDataPath)
        
## Main
if __name__ == "__main__":
    myApp = App()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["help", "input=", "verbose"])
    except getopt.GetoptError as err:
        ## Error in arguments
        print str(err)
        myApp.usage()
        sys.exit(2)

    ## Mandatory 
    inputDataPathFound = False

    #print opts

    for o, a in opts:
        if o in ("-v", "--verbose"):
            myApp.verbose = True
        elif o in ("-h", "--help"):
            myApp.usage()
            sys.exit(0)
        elif o in ("-i", "--input"):
            myApp.inputDataPath = a
            inputDataPathFound = True
        else:
            assert False, "unhandled option"
                
    ## Mandatory Check      
    if not inputDataPathFound: ## Is an input given?
        print "-i [file_path] or --input [file_path] was not given"
        myApp.usage()
        sys.exit(2)

    if not ntpath.isfile(myApp.inputDataPath): ## Is input a file?
        print "The path given as an input is not a file"
        myApp.usage()
        sys.exit(2)
    
    myApp.makeFolder()
