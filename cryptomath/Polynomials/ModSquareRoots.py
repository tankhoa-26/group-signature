from ..Factorization.Factorization import PrimeFactorizationSmall
from ..Algorithms.Algorithms import FastPower
from ..Polynomials.Polynomials import JacobiSymbol

def TonelliShanks(a, n):
  '''
  Performs the Tonelli-Shanks algorithm to find modular square roots for a mod n\n
  Inputs:
    integers a, n
  Output:
    integers x1, x2
  '''
  if JacobiSymbol(a, n) == -1:
    # There are no square roots for a mod n
    raise Exception('JacobiSymbol(): ' + str(a) + ' does not have square roots mod ' + str(n))
  s = 0
  m = n - 1
  while m % 2 == 0:
    m = m // 2
    s += 1
  # Select z such that (z/p) = -1
  z = 2
  while JacobiSymbol(z, n) == 1:
    z += 1
  # Set initial values
  e = s
  c = FastPower(z, m, n)
  x = FastPower(a, (m + 1) // 2, n)
  t = FastPower(a, m, n)
  while t > 1:
    # Find the smallest i < e such that t^(2^i) = 1 mod n
    i = 1
    while FastPower(t, 2 ** i, n) != 1:
      i += 1
    # Set values
    b = FastPower(c, FastPower(2, e - i - 1, n), n)
    x = b * x % n
    c = FastPower(b, 2, n)
    t = t * c % n
    e = i
  return x, n-x

def ModSquareRoots(a, n):
  '''
  If a is a quadratic residue mod n, return its square roots\n
  Inputs:
    integers a, n
  Output:
    integers r1, r2
  '''
  if JacobiSymbol(a, n) == -1:
    # There are no square roots for a mod n
    raise Exception('ModSquareRoots(): ' + str(a) + ' does not have square roots mod ' + str(n))

  # Check for 3 mod 4 (1 mod 8 and 7 mod 8) shortcut
  if n % 4 == 3:
    x = FastPower(a, (n + 1) // 4, n)
    return x, n-x

  # Check for 5 mod 8 shortcut
  if n % 8 == 5:
    k = n // 8
    if FastPower(a, (n - 1) // 4, n) == 1:
      x = FastPower(a, k + 1, n)
    else:
      x = FastPower(2, 2 * k + 1, n) * FastPower(a, k + 1, n)
      x = x % n
    return x, n-x

  # If 1 mod 8, perform Tonelli-Shanks
  if n % 8 == 1:
    return TonelliShanks(a, n)

  # Then n must be composite
  fact = PrimeFactorizationSmall(n)
  # Hensel's Lemma?

  return 0, 0