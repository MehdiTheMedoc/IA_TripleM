from multiprocessing import Pool

files = ["example.txt"]

def open_file(file):
	with open(file) as f:
		f = f.read()
	return f

def len_words(file):
	words = open_file(file).split()
	global words
	return len(words)

def create_buckets(file):
	x = len_words(file)/10
	return x

def split_words(l):
    return [[len(i), i] for i in l]	

def pool(file):
	b_size = create_buckets(file)
	end = b_size
	pool = Pool(processes = 10)
	start = 0
	while b_size < len(words):
		result = pool.apply_async(split_words, [words[start:end]])
		start += b_size
		if end < len(words):
			end += b_size
		else:
			end = None
			break
		print result.get()

print pool("example.txt")