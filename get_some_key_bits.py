import util
import binascii
import sys
import itertools
import operator

intab = "fghijklmnopqrstu"
outtab = "0123456789abcdef"
trantab = str.maketrans(intab, outtab)

def getbytestrings(inbytes):
  """Convert a hex string of 64 bits into a bit string of length 64"""
  return ("{0:020b}".format(int(inbytes, 16))).zfill(64)

def splitInHalf(st):
  """Split a bit string into 2 strings of half length"""
  return st[:len(st)//2], st[len(st)//2:]

def toBitList(st):
  """Convert bit string to bit list of integers"""
  return list(map(lambda x: ord(x)-ord('0'), st))

def bitListToInt(bl):
  """Convert bit list to the represented integer"""
  if bl[0] != 0 and bl[0] != 1:
    print('ALARM')
    exit(0)
  out = 0
  for bit in bl:
    out = (out << 1) | bit
  return out

def tupleToBigInt(tup):
  """Convert a tuple to an int"""
  kk = 0
  for t in tup:
    kk = kk << 6
    kk += t
  return kk

def getblock(j, bt, k):
  """Get the jth chunk of k bits"""
  return bt[k*j-k:k*j]

# Bj and Cj are bit lists
def IN(j, bj, cj):
  res = []
  for k in range(64):
    r1 = util.S[j][k]
    r2 = bitListToInt(util.xorBitList(bj, toBitList(format(k, '06b'))))
    r3 = util.S[j][r2]
    r4 = util.xorBitList(toBitList(format(r1, '04b')), toBitList(format(r3, '04b')))

    if bitListToInt(r4) == bitListToInt(cj):
      res.append(k)
  return res

# E1 E2 are 6 bit bitlists
# c is 4 bit bitList
def test(j, e1, e2, c):
  """Returns set of 6 bit ints"""
  r1 = util.xorBitList(e1, e2)
  r2 = list(map(lambda k: k ^ bitListToInt(e1), IN(j, r1, c)))
  return r2

def lookS(j, i):
  return util.S[j][(16 * (2 * (i // 32) + i % 2)) + (i // 2) % 16]

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('Wanted input file as argument')
    exit(0)

  counter = [ [0]*64 for _ in range(9) ]

  with open(sys.argv[1]) as f:
    cn = 0
    for line in f:
      # if cn > 0:
        # break
      # cn = cn + 1

      line = line.rstrip().split(' ')
      line[0] = line[0].translate(trantab).replace(':', '')
      line[1] = line[1].translate(trantab).replace(':', '')

      in0, in1 = splitInHalf(line[0])
      out0, out1 = splitInHalf(line[1])

      pout0 = ''.join(util.applyBitPermutation(util.rfpinv, list(getbytestrings(out0))))
      pout1 = ''.join(util.applyBitPermutation(util.rfpinv, list(getbytestrings(out1))))

      def helper(k):
        a, b = k
        return toBitList(a), toBitList(b)

      # All 4 are bit lists
      lf0, rf0 = helper(splitInHalf(pout0))
      lf1, rf1 = helper(splitInHalf(pout1))

      # Is a bit list
      cons = toBitList(''.join(map(util.byteToBitString, util.xor))[32:])

      # Are bit lists
      rPrime = util.xorBitList(rf0, rf1)
      cPrime = util.applyBitPermutation(util.pinv, util.xorBitList(rPrime, cons))

      e0 = util.expand(lf0)
      e1 = util.expand(lf1)

      co1 = [] # Inputs that go into S box for 1st plaintext
      co2 = [] # Inputs that go into S box for 2nd plaintext
      c = []
      for j in util.sBoxesForThisXor:
        co1.append(bitListToInt(getblock(j, e0, 6)))
        co2.append(bitListToInt(getblock(j, e1, 6)))
        c.append(bitListToInt(getblock(j, cPrime, 4)))

      # First guess a 6 bit value
      for k in range(64):
        # Try that for each S box relevant for this XOR value
        for i in range(len(util.sBoxesForThisXor)):
          # If the input and output match
          if (lookS(util.sBoxesForThisXor[i], co1[i] ^ k) ^
              lookS(util.sBoxesForThisXor[i], co2[i] ^ k)) == c[i]:
            # Increment the counter for this guessed value
            counter[util.sBoxesForThisXor[i]][k] += 1

  def getmaxindex(lis):
    m = max(lis)
    return [i for i, j in enumerate(lis) if j==m]

  for j in util.sBoxesForThisXor:
    # The value with the max occurance wins
    print(j, getmaxindex(counter[j]))
