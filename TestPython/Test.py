##size = 59
##
##a = range(size)
##
##nbThread = 7
##
##print float(size) / nbThread
##print a
##for i in range(nbThread):
##    print "i = %d" % i
##    min = int(i * float(size) / nbThread)
##    print "min %d" % min
##    max = int((i+1) * float(size) / nbThread -1 )
##    print "max %d" % max
##    print a[min:max+1]

for i in range(5,9):
    print i
