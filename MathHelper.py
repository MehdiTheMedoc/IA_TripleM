def arrayProduct(a,b):
    if len(a) != len(b):
        print "Warning : Returning None in arrayProduct() %d!=%d" % (len(a),len(b))
        return None

    tmp = [ a[i] * b[i] for i in range(len(a)) ]
    res = 0
    for i in range(len(tmp)):
        res += tmp[i]

    return res
        

if __name__ == '__main__':
	a = [1,2,3,4,5]
	b = [9,8,7,6,5]

	print a
	print b
	print arrayProduct(a,b)
	
	raw_input('Press Start \r\n')