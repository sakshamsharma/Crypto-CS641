import itertools
import random

import util

intab = "0123456789abcdef"
outtab = "fghijklmnopqrstu"
trantab = str.maketrans(intab, outtab)

# The final permuted xor to be used
permuxor = util.applyPermutation(util.ipinv, util.xor)

# Required pairs
req = 1000000

def convert(hexlist):
  """Print the list of 8 bytes as a string for input"""
  st = ''
  for op in hexlist:
    st += ('%02x' % op)
  # Result as hex using fghijklmnopqrstu instead of 0123456789abcdef
  return st.translate(trantab)

def basexor(base):
  """XOR 64 bits with the required XOR"""
  return [x ^ y for (x, y) in zip(base, permuxor)]

def randombytes():
  """Get 8 random bytes, i.e. 64 bits"""
  for i in range(8):
    yield random.randint(0, 255)

def test(s1, s2):
  """Test if XOR of byte arrays s1 and s2 is what you wanted"""
  x1 = util.applyPermutation(util.ip, s1)
  x2 = util.applyPermutation(util.ip, s2)
  res = [ x ^ y for (x, y) in zip(x1, x2) ]
  st = ''
  for op in res:
    st += ('%02x' % op)
  return st

cnt = 0
while True:
  base = list(randombytes())
  toprint = convert(base) + ' ' + convert(basexor(base))
  print(toprint)
  # print(test(base, basexor(base)))
  cnt = cnt + 1

  if cnt > req:
    break
