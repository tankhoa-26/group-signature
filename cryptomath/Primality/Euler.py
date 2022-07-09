# Primality testing based on Euler's Criterion

from ..Polynomials.Polynomials import JacobiSymbol
from ..Algorithms.Algorithms import FastPower
from random import randint

def EulerTest(a, n):
  '''
  Performs the Euler Test to see if Euler's Criterion holds such that a^((n-1)/2) is congruent to the Jacobi Symbol of a mod n\n
  Inputs:
    integers a, n
  Output:
    boolean e (false if composite, true if "probably prime")
  '''
  f = FastPower(a, (n-1)//2, n)
  if f == n - 1:
    f = -1
  j = JacobiSymbol(a, n)
  return f == j

def SolovayStrassenTest(n, tries=10):
  '''
  Performs the Solovay-Strassen Test on possible prime n\n
  Inputs:
    integers n, tries (optional, default: 10)
  Outputs:
    boolean s (false if composite, true if "probably prime")
  '''
  # Use EulerTest to test random integers
  bound = n + 1
  if tries > n - 2:
    bound += tries
  for i in range(tries):
    a = randint(2, bound)
    if not EulerTest(a, n):
      # Found a witness for the compositeness of n
      return False
  return True