# Additional algorithms that may be relevant to specific functions

def HammingWeight(x):
  '''
  Determines the Hamming Weight of an integer, or the number of 1s in the binary representation of that number\n
  Input:
    integer x
  Output:
    integer h
  '''
  h = 0
  while x:
    h += 1
    x &= x - 1
  return h
