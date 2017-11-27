import os, time, random, sys, getopt, ntpath

import MathHelper

verbose = False
x = y = tetha = []
alpha = n = e = trainTime = 0
workingFolder = fileName = ext = startTime = saveFolder = logsFile = loadFile = 'poney'

def usage():
    print "toDo Usage()"

def customReplace(string, olds, new=''):
    for old in olds:
        string.replace(old,new)
    return string

def readData(filename):
    global verbose
    global workingFolder, fileName, ext, startTime, saveFolder, logsFile, loadFile
    
    print ext
    
    f = open(filename, 'r+')

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

    return lineCount, dataCount, x, y

def save(theta, filename):
    f = open(filename, 'r+')

    f.write(str(i))
    f.close
    
    
def train(dataFile):
##    e = 15 # nb of example
##
##    n = 3 # nb of data analyze (weight, length, power)
##    
##    n += 1 # pour le threshold
##
##    theta = [ 0 for i in range(n)]

    alpha = 0.000005

##    x = [[ random.random() for i in range(n)] for j in range(e)]
##    for i in range(len(x)):
##        x[i][0] = 1 # Threshold, only theta is taken into account
##    print x[0]
##    y = [ random.random() for j in range(e)]

    
    print "Debug : reading file"
    e,n,x,y = readData(dataFile)
    theta = [ 0 for i in range(n)]
    print theta
    print "Debug : reading done"

    # print "Debug"
    # print x
    # print y
    # print "Debug end"

    print "Debug : training..."
    # training theta
    for time in range(50): #redo the train x times
        for i in range(e): #each example
            for j in range(n): #each data type

                # update the corresponding theta
                sumDerivated = 0

                for t in range(e):
                    sumDerivated += (MathHelper.arrayProduct(theta, x[t]) - y[t]) * x[t][j]
            
                theta[j] -= alpha * ( float(1) / e ) * sumDerivated

            # print theta
        print theta
    print "Debug : training done!"


    print "Debug : testing..."
    # print MathHelper.arrayProduct(theta, [1,49.94357,21.47114,73.07750,8.74861,-17.40628,-13.09905,-25.01202,-12.23257,7.83089,-2.46783,3.32136,-2.31521,10.20556,611.10913,951.08960,698.11428,408.98485,383.70912,326.51512,238.11327,251.42414,187.17351,100.42652,179.19498,-8.41558,-317.87038,95.86266,48.10259,-95.66303,-18.06215,1.96984,34.42438,11.72670,1.36790,7.79444,-0.36994,-133.67852,-83.26165,-37.29765,73.04667,-37.36684,-3.13853,-24.21531,-13.23066,15.93809,-18.60478,82.15479,240.57980,-10.29407,31.58431,-25.38187,-3.90772,13.29258,41.55060,-7.26272,-21.00863,105.50848,64.29856,26.08481,-44.59110,-8.30657,7.93706,-10.73660,-95.44766,-82.03307,-35.59194,4.69525,70.95626,28.09139,6.02015,-37.13767,-41.12450,-8.40816,7.19877,-8.60176,-5.90857,-12.32437,14.68734,-54.32125,40.14786,13.01620,-54.40548,58.99367,15.37344,1.11144,-23.08793,68.40795,-1.82223,-27.46348,2.26327])
    print MathHelper.arrayProduct(theta, [1, 626,626])
    print "Debug : many wow!"

    #raw_input('Press Start \r\n')
    sys.exit("Bye !!")
    
    
##    filename = "poney.txt"
##
##    f = open(filename, 'r+')
##    i = int(f.read())
##    
##    while True: 
##        try:
##            i += 1
##
##            f.seek(0)
##            f.write(str(i))
##            f.truncate()
##            str_error = None
##        except Exception as str_error:
##            pass
##
##        if str_error:
##            print 'Quiting driver'
##            driver.quit()
##            print str_error
##            raw_input('Press Start')
##            sys.exit("Bye !!")

def arguments():
    try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help", "input=", "output=", "verbose"])
    except getopt.GetoptError as err:
            ## Error in arguments
            print str(err)
            usage()
            sys.exit(2)

    ## Default arguments
    
    
    inputDataPath = 'example.txt'
    outputDataPath = 'exampleOutput.txt'
    logDataPath = 'exampleLog.txt'
    verbose = False

    ## Mandatory 
    inputDataPathFound = False
    outputDataPathFound = False
    logDataPathFound = False

    #print opts

    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-i", "--input"):
            inputDataPath = a
            inputDataPathFound = True
        #elif o in ("-o", "--output"):
           #outputDataPath = a
           #outputDataPathFound = True
        #elif o in ("-l", "--log"):
            #logDataPath = a
            #logDataPathFound = True
        else:
            assert False, "unhandled option"
                
    ## Mandatory Check      
    if not inputDataPathFound: ## Is an input given?
        print "-i [file_path] or --input [file_path] was not given"
        usage()
        sys.exit(2)

    if not ntpath.isfile(inputDataPath): ## Is input a file?
        print "The path given as an input is not a file"
        usage()
        sys.exit(2)

    ## Folder/File/Ext Names
    workingFolder, fileName = ntpath.split(inputDataPath)
    #fileName = ntpath.basename(inputDataPath) if '.' not in ntpath.basename(inputDataPath) else ntpath.basename(inputDataPath)
    fileName, ext = ntpath.splitext(fileName)
    #startTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    startTime = time.strftime("%x_%X")
    saveFolder = ntpath.join(workingFolder, fileName) + "Results"
    logsFile = startTime + "_Logs"
    loadFile = startTime + "_Load"
    
    if verbose:
        print "Starting Time : " + startTime
        print "workingFolder : " + workingFolder
        print "saveFolder : " + saveFolder
        print "fileName : " + fileName
        print "ext : " + ext

    ## Make dir
    if not ntpath.isdir(saveFolder):
        os.makedirs(saveFolder)            

    train(inputDataPath)

if __name__ == "__main__":
    arguments()
