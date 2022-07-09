# Additional algorithms using factorization that may be useful

from .Factorization import PrimeFactorization

def SquareFree(x):
  '''
  Determines if an integer is squarefree (if its factorization contains no squares besides 1)\n
  Input:
    integer x
  Output:
    boolean s
  '''
  fact = PrimeFactorization(x)
  for f in fact:
    if f[1] > 1:
      return False
  return True

def Totient(x):
  '''
  Computes Euler's Totient/Phi function on x, or the number of positive integers less than x that are coprime to x\n
  Input:
    integer x
  Output:
    integer t
  '''
  if x == 0:
    return 1
  if x == 1:
    return 1
  fact = PrimeFactorization(x)
  for f in fact:
    x *= (1 - (1/f[0]))
  return round(x)
