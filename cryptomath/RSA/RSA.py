# Implementation of the RSA cryptosystem

from secrets import randbelow
from ..Generators.Generators import GenerateProbablePrime
from math import log2, floor
from ..Algorithms.Algorithms import GCD, ModularInv
from ..Algorithms.AdditionalAlgorithms import HammingWeight


def RSA_Public_KeyGen(length, pubout, privout):
  '''
  Creates a large semiprime of a specified length, and creates a public and private key pair.\n
  Inputs:
    integer length (bit length of modulus, ex. 1024, 2048, 4096)
    string pubout (public key output filename)
    string privout (private key output filename)
  Outputs:
    files pubout (.key), privout (.key)
  '''
  # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Operation

  if length < 1024:
    raise('Modulus bit length must be at least 1024')
  if log2(length) != floor(log2(length)):
    raise('Modulus bit length must be a power of 2')

  print('Creating RSA key pair for bit length of ' + str(length) + ':')
  print('Generating modulus...')

  # Generate two distinct primes p and q
  # p and q should slightly differ in length to prevent guessing ~sqrt(n)
  offset = randbelow(length // 10)
  p = GenerateProbablePrime(length // 2 - offset)
  q = GenerateProbablePrime(length // 2 + offset)
  n = p * q
  # Compute the totient
  phi = (p-1) * (q-1)
  # Pick a public e
  # Must be 1<e<phi, gcd(phi,e)=1
  # Ideally, e has a short bit-length and small Hamming weight
  print('Generating e...')
  while True:
    # Generate random below ~2^(length/2)
    e = randbelow(phi // (2 ** (floor(log2(phi)) // 2)))
    if (e < 3):
      continue
    if GCD(phi, e) == 1:
      break
  # Compute private d
  print('Computing d...')
  d = ModularInv(e, phi)

  return n, e, d