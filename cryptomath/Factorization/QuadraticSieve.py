# Implementation of the Quadratic Sieve algorithm

from math import exp, floor, sqrt, log10
from ..Primality.Primality import IsPrime
from ..Polynomials import JacobiSymbol
from ..Generators import GeneratePrimes
from ..Algorithms.Algorithms import GCD

base = []
table = []

def QuadraticSieve(n):
  '''
  Finds a nontrivial factor of n using the Quadratic Sieve algorithm\n
  Input:
    integer n
  Output:
    integer f (a single factor)
  '''
  raise Exception('Function QuadraticSieve() not yet implemented')
  return 0

def NaiveQuadraticSieve(n):
  global base

  # Set bounds for factor base
  B = floor(L(n) ** (1/sqrt(2)))
  # Create factor base
  beta = GeneratePrimes(B)
  # Remove quadratic nonresidues
  base = [b for b in beta if JacobiSymbol(b, n) == 1]
  # Get estimate for values to look around
  x = floor(sqrt(n)) + 1
  table = []
  indices = []
  # Begin looking...
  while True:
    y = x ** 2 - n
    # We would like a y expressable as a combination of primes from our base
    expressible, factorization = FactorY(y)
    if expressible:
      table.append([x, y, factorization, Mod2(factorization)])
      sq, indices = IsSquare(table[3])
      if sq:
        break
  # We've found multiple y which combine as a square
  X = 0
  Y = 0
  for i in indices:
    X *= table[0][i]
    Y *= table[1][i]
  Y = sqrt(Y)
  if floor(Y) != Y:
    raise Exception('NaiveQuadraticSieve(): Failure: Y is not a square')
  else:
    g = GCD(X - Y, n)
    if g > 1:
      return g
    else:
      raise Exception('NaiveQuadraticSieve(): Failure: Found trivial factor (1)')

def FactorY(y):
  '''
  Factors y as a combination of primes in the factor base
  Returns boolean representing pass/fail, and the factorization vector (upon success)
  '''
  global base
  index = 0
  factorization = [0] * len(base)
  while y > 1:
    while y % base[index]:
      y /= base[index]
      factorization[index] += 1
    if y < base[index] or index == len(base) - 1:
      return False, []
    index += 1
  return True, factorization

def Mod2(li):
  '''
  Returns li mod 2
  '''
  for i in range(len(li)):
    li[i] = li[i] % 2
  return li

def IsSquare(table):
  '''
  Combined multiple mod2 lists to see if there are any combinations that are squares
  If square, return indices of columns that create the square
  '''
  raise Exception('Function IsSquare() not yet implemented')
  return False, []

def L(x):
  return exp(sqrt(log10(x) * log10(log10(x))))
