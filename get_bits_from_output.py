import util
import binascii
import sys
import itertools
import operator

intab = "fghijklmnopqrstu"
outtab = "0123456789abcdef"
trantab = str.maketrans(intab, outtab)

if len(sys.argv) < 2:
  print('Wanted input file as argument')
  exit(0)

def getbytestrings(inbytes):
  return ("{0:020b}".format(int(inbytes, 16))).zfill(64)

def splitInHalf(st):
  return st[:len(st)//2], st[len(st)//2:]

def toBitList(st):
  return list(map(lambda x: ord(x)-ord('0'), st))

def bitListToInt(bl):
  out = 0
  for bit in bl:
    out = (out << 1) | bit
  return out

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

def tupleToBigInt(tup):
  kk = 0
  for t in tup:
    kk = kk << 6
    kk += t
  return kk

myhashmap = {}

with open(sys.argv[1]) as f:
  for line in f:
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
    cons = toBitList(''.join(map(util.byteToBitString, util.xor))[:32])

    # Are bit lists
    rPrime = util.xorBitList(rf0, rf1)
    cPrime = util.applyBitPermutation(util.pinv, util.xorBitList(rPrime, cons))

    e0 = util.expand(lf0)
    e1 = util.expand(lf1)

    def getblock(j, bt, k):
      return bt[k*j-k:k*j]

    doomed = False
    boom = []
    for j in [2, 5, 6, 7, 8]:
      res = test(j, getblock(j, e0, 6), getblock(j, e1, 6), getblock(j, cPrime, 4))
      if res == []:
        doomed = True
        break
      boom.append(res)

    if doomed:
      continue

    # By now boom has 5 6-bit integers ki list
    # And kk will have their cartesian product
    kk = itertools.product(*boom)
    for k in kk:
      bb = tupleToBigInt(k)
      myhashmap.setdefault(bb, 0)
      myhashmap[bb] += 1

cnt = 0
for (k, v) in sorted(myhashmap.items(), key=operator.itemgetter(0)):
  cnt = cnt + 1
  print(k, v)
  if cnt > 10:
    break
