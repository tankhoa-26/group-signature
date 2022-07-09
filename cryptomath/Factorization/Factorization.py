# Factoring numbers using various techniques

from .Pollard import Pollard, PollardP_1
from .Lenstra import Lenstra
from .QuadraticSieve import QuadraticSieve
from math import log10, floor
from ..Primality.Primality import IsPrime

def PrimeFactorization(n):
  '''
  Returns a list of the prime factorization of n, giving factors and exponents
  Input:
    integer n
  Output:
    list of tuples of integers (factor, exponent)
  '''
  factors = Factors(n, True)
  pf = []
  pf.append([factors[0],1])
  for fac in factors[1:]:
    if pf[-1][0] == fac:
      pf[-1][1] += 1
    else:
      pf.append([fac,1])
  return pf

def Factors(n, dup=False):
  '''
  Returns a list of the factors of n
  Input:
    integer n
    (optional) dup - include duplicate factors
  Output:
    list of integers f
  '''
  # Using the following link for guidance...
  # https://stackoverflow.com/questions/2267146/what-is-the-fastest-factorization-algorithm

  if IsPrime(n):
    return [n]

  def FactorRecursive(n):
    length = floor(log10(n))
    #print('Recursive: factoring ' + str(n) + ', ' + str(length) + ' digits')

    if length <= 21:
      # Use Pollard's
      factor = Pollard(n)
      if factor == -1:
        factor = PollardP_1(n)
    elif length <= 50:
      # Use Lenstra's
      factor = Lenstra(n)
    elif length <= 100:
      # Use Quadratic Sieve
      factor = QuadraticSieve(n)
    else:
      # Use General Number Field Sieve
      raise Exception('Factors(): Number is too big to factor')

    if factor == -1:
      raise Exception('Factor(): Failure to find a factor for ' + str(n))

    factor2 = n // factor
    if IsPrime(factor2):
      return [factor, factor2]
    else:
      return [factor] + FactorRecursive(factor2)

  factors = FactorRecursive(n)
  factors.sort()

  if dup:
    return factors

  factors2 = []
  for f in factors:
    if not f in factors2:
      factors2.append(f)

  return factors2