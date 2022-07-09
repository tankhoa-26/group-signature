# Number generators

from ..Primality.Primality import MillerRabin, IsPrime
import threading
from secrets import randbits

possibleNum = 0
#count = 0

def genNum(length, lock):
  global possibleNum
  #global count
  while not possibleNum:
    x = randbits(length)
    #lock.acquire()
    #try:
    #  count += 1
    #finally:
    #  lock.release()
    if MillerRabin(x):
      lock.acquire()
      try:
        possibleNum = x
      finally:
        lock.release()
  #print(str(threading.get_ident()) + ' closing, count=' + str(count))

def GenerateProbablePrimeThreaded(length):
  '''
  Generates a random prime number of a specified binary length
  Input:
    integer length
  Output:
    integer p
  '''
  global possibleNum
  #global count
  possibleNum = 0 # reset
  lock = threading.Lock() # mutex lock to prevent race conditions
  threadNum = 2 # number of threads to spawn to generate number/primality pairs

  # Create list of threads
  threads = [threading.Thread(daemon=True, target=genNum, args=(length,lock)) for i in range(threadNum)]
  # Execute threads concurrently
  [thread.start() for thread in threads]
  [thread.join() for thread in threads]

  #print('Count: ' + str(count))

  return possibleNum

def GenerateProbablePrime(length):
  '''
  Generates a random prime number of a specified binary length, not multithreaded
  Input:
    integer length
  Output:
    integer p
  '''
  x = randbits(length)
  if x % 2 == 0:
    x += 1
  while True:
    if MillerRabin(x):
      return x
    x += 2

def GeneratePrimes(n):
  '''
  Generates all primes below n
  Input:
    integer n
  Output:
    list of integers
  '''
  return [x for x in range(n) if IsPrime(x)]