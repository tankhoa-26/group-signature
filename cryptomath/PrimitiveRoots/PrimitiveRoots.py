# Functions relating to primitive roots
from ..Polynomials.Polynomials import JacobiSymbol
from ..Primality.Primality import IsPrime
from ..Factorization.Factorization import Factors, PrimeFactorization
from ..Algorithms.Algorithms import FastPower, GCD

def Order(a, n):
  '''
  Computes orda(n), or the smallest integer m such that a^m = 1 (mod n)\n
  Inputs:
    integers a, n such that GCD(a, n) = 1
  Output:
    integer ord
  '''
  if GCD(a, n) != 1:
    raise Exception('Order(): a and n must be coprime')
  x = 1
  while FastPower(a, x, n) != 1:
    x += 1
  return x

def IsPrimRoot(g, p, fact=[]):
  '''
  Computes whether g is a primitive root p, or if g generates the entire group Zp
  Inputs:
    integers g, p
    list of integers fact (optional)
  Output:
    boolean pr
  '''
  if JacobiSymbol(g, p) != -1 or g == 0:
    return False
  if IsPrime(p):
    # Usual case
    if len(fact) == 0:
      fact = Factors(p-1)
    for f in fact:
      if FastPower(g, (p-1)//f, p) == 1:
        return False
    return True
  else:
    # Can only be a prim root if the modulo is of the form 
    # p^k or 2p^k with an odd prime
    fact = PrimeFactorization(p)
    if len(fact) == 1:
      # Of the form p^k
      pr = fact[0][0]
      if IsPrimRoot(g, pr):
        return FastPower(g, pr-1, pr ** 2) != 1
    elif len(fact) == 2 and fact[0] == [2,1]:
      # Of the form 2p^k
      # If g is a prim root mod p^k and is odd, it is also a prim root of 2p^k
      if g % 2 == 1:
        return IsPrimRoot(g, fact[1][0])
    return False

def PrimRoots(p):
  '''
  Find all primitive roots for p
  Input:
    integer p
  Output:
    list of integers
  '''

  def findOtherPrimRoots(r, p):
    roots = [r]
    for i in range(p-1):
      if GCD(i, p-1) == 1:
        x = FastPower(r, i, p)
        if not x in roots:
          roots.append(x)
    roots.sort()
    return roots

  def findOnePrimRoot(p):
    r = 2
    fact = Factors(p-1)
    while not IsPrimRoot(r, p, fact):
      r += 1
    return r

  # There should be exactly phi(phi(p)) primitive roots
  # Find one primitive root first
  if IsPrime(p):
    return findOtherPrimRoots(findOnePrimRoot(p), p)
  else:
    if p == 2:
      return [1]
    elif p == 4:
      return [3]
    print('Function PrimRoots() is unfinished for a composite integer')
    fact = PrimeFactorization(p)
    # p^k
    if len(fact) == 1:
      pr = fact[0][0]
      g = findOnePrimRoot(pr)
      print(g)
      if FastPower(g, pr-1, pr ** 2):
        return findOtherPrimRoots(g+pr, p)
      return findOtherPrimRoots(g, p)
    # 2p^k
    elif len(fact) == 2 and fact[0] == [2,1]:
      pr = fact[1][0]
      g = findOnePrimRoot(p)
      if FastPower(g, pr-1, pr ** 2):
        g += pr
      # Found a prim root mod p^k, now find for 2p^k
      if g % 2 == 1:
        return findOtherPrimRoots(g, p)
      return findOtherPrimRoots(g + (pr ** fact[1][1]), p)
    else:
      return []
