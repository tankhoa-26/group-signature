from cgi import print_arguments
import multiprocessing as mp
import math
import secrets
import threading
import utils
from cryptomath.Primality.Primality import IsPrime, IsSophieGermainPrime
global primes
primes =[]

global k
k = 2
two_pow_l_p = utils.square_and_multiply(2, 512)


# Check all the numbers from startPos, 1 by 1, to find prime numbers
def run( lock):
    global k
    n = secrets.randbelow(two_pow_l_p)
    while k > 0:
        print("k: ",k)
        
        if IsSophieGermainPrime(n):
            #lock.acquire()
            primes.append(n)
            k-=1
            print("n: ",n)
            #lock.release()
        else:
            n = secrets.randbelow(two_pow_l_p)
        


#Main Program Starts Here...
#Let's intialise three different threads.Each thread will be used to dientify prime numbers starting with a different starting position
def mainTask():
    global k
    k = 2
    lock = threading.Lock()

    thread1 = threading.Thread(target=run, args=(lock,))
    thread2 = threading.Thread(target=run, args=(lock,))
    thread3 = threading.Thread(target=run, args=(lock,))

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()



#Let's start our three threads to implement concurrent processing!
mainTask()
print("result: ")
for i in range (len(primes)):
    print(primes[i])
