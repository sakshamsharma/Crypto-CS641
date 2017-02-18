import itertools

ip = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
    ]

ipinv = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
    ]

def applyBitPermutation(permu, array):
  """Apply given permutation to bit array"""

  # Final result will be stored in this
  permubitxor = array[:]
  for i, c in enumerate(permubitxor):
    permubitxor[i] = array[permu[i]-1]

  return permubitxor

def applyPermutation(permu, array):
  """Apply given permutation to array"""

  # Gives you a bit array for the above defined xor
  bitxor = list(
      itertools.chain.from_iterable(map(lambda x: bin(x)[2:].rjust(8, '0'), array)))

  # Final result will be stored in this
  permubitxor = bitxor[:]
  for i, c in enumerate(permubitxor):
    permubitxor[i] = bitxor[permu[i]-1]

  def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
          yield l[i:i + n]

  permuxor = list(chunks(permubitxor, 8))
  return list(map(lambda x: (int(''.join(map(lambda y: str(y), x)), 2)), permuxor))

xor = [ 0x40, 0x08, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00 ]
# xor = [ 0x00, 0x20, 0x00, 0x08, 0x00, 0x00, 0x04, 0x00 ]
# xor = [ 0x40, 0x5C, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00 ]

