import sys, getopt, ntpath

def doMagic(inputDataPath, outputDataPath):
    if(False):
        print 'Starting Magic...'
    
    #newFileDataPath = ntpath.basename(inputDataPath).split('.')[0]
    
    textFile = open(inputDataPath, 'r+')
    otherFile = open(outputDataPath,'w+')

    i = 0
    for line in textFile:
        i += 1
        otherFile.write(line)
        if(False and i % 10000 == 0):
           print 'Copying Line ' + str(i) + '!'

    textFile.close()
    otherFile.close()

    if(False):
        print 'Magic Done...'

if __name__ == "__main__":
    try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help", "input=", "output="])
    except getopt.GetoptError as err:
            ## Error in arguments
            print str(err)
            print "TextToFile.py -f [someFile.someExt] -o [someOtherFile.someOtherExt]"
            sys.exit(2)

    # Mandatory 
    inputDataPathFound = False
    outputDataPathFound = False
   
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            print "TextToFile.py -f [someFile.txt]"
            sys.exit(0)
        elif o in ("-i", "--input"):
            inputDataPath = a
            inputDataPathFound = True
        elif o in ("-o", "--output"):
            outputDataPath = a
            outputDataPathFound = True
        else:
            assert False, "unhandled option"

    if not inputDataPathFound:
        print "text file path was not given"
        print "TextToFile.py -f [someFile.txt]"
        sys.exit(2)
    if not outputDataPathFound:
        print "text file path was not given"
        print "TextToFile.py -f [someFile.txt]"
        sys.exit(2)

    doMagic(inputDataPath,outputDataPath)
