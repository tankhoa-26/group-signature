# Polynomial operations in modular arithmetic

from ..Algorithms.Algorithms import GCD
from ..Primality.Primality import IsPrime
from ..Factorization.Pollard import PrimeFactorizationSmall
from math import sqrt, floor
from ..Algorithms.Algorithms import FastPower

def JacobiSymbol(a, n):
  '''
  Finds the Jacobi Symbol (a / n) of an integer a mod n\n
  Inputs:
    integers a, n
  Output:
    integer j in [-1,0,1]
  '''

  def LegendreSymbol(a, n):
    while True:
      if n % 2 == 0:
        raise Exception('LegendreSymbol(): Legendre Symbols are undefined for even mods')

      # Reduce a mod n
      a = a % n

      # if a is a square, (a/n) gives +1
      s = sqrt(a)
      if s == floor(s):
        return 1

      # (-1/n) = (-1)^((n-1)/2)
      elif a == n - 1:
        return floor((-1) ** ((n-1)/2))

      # (2/n) gives +1 for n = 1,7 mod 8, -1 for n = 3,5 mod 8
      elif a == 2:
        if n % 8 == 1 or n % 8 == 7:
          return 1
        return -1

      # (-3/n) gives +1 for n = 1 mod 6, -1 for n = 5 mod 6
      elif a == n - 3:
        if n % 6 == 1:
          return 1
        elif n % 6 == 5:
          return -1

      # (5/n) gives +1 for n = 1,9 mod 10, -1 for n = 3,7 mod 10
      elif a == 5:
        if n % 10 == 1 or n % 10 == 9:
          return 1
        elif n % 10 == 3 or n % 10 == 7:
          return -1
      
      # if a,n odd, (a/n) gives -(n/a) if a,n = 3 mod 4, (n/a) otherwise
      elif a % 2 == 1:
        if a % 4 == 3 and n % 4 == 3:
          return LegendreSymbol(n, a) * -1
        else:
          return LegendreSymbol(n, a)

      # (ab/n) = (a/n)(b/n)
      elif not IsPrime(a):
        factorization = PrimeFactorizationSmall(a)
        parts = []
        for fac in factorization:
          if fac[1] % 2 == 0:
            # factor is a square, symbol is 1
            continue
          else:
            for i in range(fac[1]):
              parts.append(fac[0])
        symbol = 1
        for p in parts:
          symbol *= LegendreSymbol(p, n)
        return symbol

      else:
        raise Exception('LegendreSymbol(): unknown error')

  a = a % n
  if GCD(a, n) > 1:
    return 0
  elif n % 2 == 0:
    if a == 1 and n == 2:
      return 1
    else:
      raise Exception('JacobiSymbol(): Jacobi Symbols are undefined for even mods')
  elif not IsPrime(n):
    # For a composite n, the Jacobi symbol is defined as:
    # (a / n) = (a / p1)^e1 * (a / p2)^e2 * ...
    factorization = PrimeFactorizationSmall(n)
    symbol = 1
    for factor in factorization:
      symbol *= LegendreSymbol(a, factor[0]) ** factor[1]
    return symbol
  else:
    return LegendreSymbol(a, n)

def IsModSquare(a, n):
  '''
  Determines if a is a square mod n\n
  Inputs:
    integers a, n
  Output:
    boolean s
  '''
  return JacobiSymbol(a, n) == 1