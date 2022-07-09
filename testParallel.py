import secrets
import threading
import utils
from cryptomath.Primality.Primality import  IsSophieGermainPrime

global primes
primes =[]
two_pow_l_p = utils.square_and_multiply(2, 512)


# Check all the numbers from startPos, 1 by 1, to find prime numbers
def run1( lock):
    global k
    n = secrets.randbelow(two_pow_l_p)
    while True:
        if IsSophieGermainPrime(n):
            lock.acquire()
            primes.append(n)
            print("n: ",n)
            lock.release()
            break
        else:
            n = secrets.randbelow(two_pow_l_p)
        
def run2( lock):
    global k
    n = secrets.randbelow(two_pow_l_p)
    while True:
        if IsSophieGermainPrime(n):
            lock.acquire()
            primes.append(n)
            print("n: ",n)
            lock.release()
            break
        else:
            n = secrets.randbelow(two_pow_l_p)

#Main Program Starts Here...
#Let's intialise three different threads.Each thread will be used to dientify prime numbers starting with a different starting position
def mainTask():
    lock = threading.Lock()

    thread1 = threading.Thread(target=run1, args=(lock,))
    thread2 = threading.Thread(target=run1, args=(lock,))
    thread3 = threading.Thread(target=run2, args=(lock,))
    thread4 = threading.Thread(target=run2, args=(lock,))   

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()



#Let's start our three threads to implement concurrent processing!
mainTask()
print("result: ")
print(primes[0])