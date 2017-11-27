import time, random, sys
import numpy as np

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# with concurrent.futures.ProcessPoolExecutor() as executor:
    # for a, res in ((a, executor.submit(processPattern, a, b, c)) for pattern in patterns):
        # print('%d is starts at: %s' % (a, res.result()))

 # with ProcessPoolExecutor() as executor:
        # for c, fut in [(c, executor.submit(process, c, 'b')) for c in 'testing']:
            # print(c, fut.result())

def multiprocessing2Args(func, args, workers):
    with ProcessPoolExecutor(workers) as executor:
        fullres = []
        for arg1, worker in [(arg1, executor.submit(func, arg1, arg2)) for arg1, arg2 in args ]:
            fullres.append(worker.result())
        # print(fullres)
    return list(fullres)
    
def multiprocessing(func, args, workers):
    with ProcessPoolExecutor() as executor:
        res = executor.map(func, args, random.random())
    return list(res)
    
    
def multithreading(func, args, workers):
    with ThreadPoolExecutor() as executor:
        res = executor.map(func, args, random.random())
    return list(res)
    
def cpu_heavy(n,m):
    # print("do %s" % str(m))
    count = 0
    for i in range(n):
        count += int(random.random()*1000)
    return count
        
def io_heavy(text):
    f = open('output.txt', 'wt', encoding='utf-8')
    f.write(text)
    f.close()

def expenser_tester(num):
    A=np.random.rand(10*num) # creation of a random Array 1D
    for k in range(0,len(A)-1): # some useless but costly operation
        A[k+1]=A[k]*A[k+1] 
    return A
    
## Main
if __name__ == "__main__":
    n = int(sys.argv[1])
    
   
    
    tmp = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    # text = str([tmp[int(random.random()*len(tmp))] for i in range(n)])
    text = tmp
    
    fa = cpu_heavy
    fb = io_heavy
    
    doTime = 5
    
    nbWorker = 1
    
    # start = time.time()
    # multiprocessing(fa, [(n,5) if (i%2) == 0 else (n,10) for i in range(n)], nbWorker)
    # print("multiprocessing in %f with %d worker" % (time.time() - start, nbWorker))

    
    for nbWorker in [1,2,4,8,16,32]:
        start = time.time()
        multiprocessing(fa, [(n,5) if (i%2) == 0 else (n,10) for i in range(n)], nbWorker)
        print("multiprocessing in %f with %d worker" % (time.time() - start, nbWorker))
        
    
    # for nbWorker in [1,2,4,8,16,32]:
        # start = time.time()
        # multiprocessing(fa, [n for i in range(doTime)], nbWorker)
        # print("multiprocessing in %f with %d worker" % (time.time() - start, nbWorker))
        # start = time.time()
        # multithreading(fa, [n for i in range(doTime)], nbWorker)
        # print("multithreading in %f with %d worker" % (time.time() - start, nbWorker))
        # print("=======================================")
        
    # print("CPU_HEAVY") # <== process should win!!
    # start = time.time()
    # for i in range(doTime):
        # fa(n)
    # print("basic in %f" % (time.time() - start))
    # start = time.time()
    # multiprocessing(fa, [n for i in range(doTime)], 8)
    # print("multiprocessing in %f" % (time.time() - start))
    # start = time.time()
    # multithreading(fa, [n for i in range(doTime)], 8)
    # print("multithreading in %f" % (time.time() - start))
    
    # print("IO_HEAVY")
    # start = time.time()
    # fb(text)
    # print("basic in %f" % (time.time() - start))
    # start = time.time()
    # multiprocessing(fb, [text], 8)
    # print("multiprocessing in %f" % (time.time() - start))
    # start = time.time()
    # multithreading(fb, [text], 8)
    # print("multithreading in %f" % (time.time() - start))