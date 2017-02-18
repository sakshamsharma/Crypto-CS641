import util
import binascii
import sys

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

    lf0, rf0 = helper(splitInHalf(pout0))
    lf1, rf1 = helper(splitInHalf(pout1))

    cons = toBitList(''.join(map(util.byteToBitString, util.xor))[:32])

    rPrime = util.xorBitList(rf0, rf1)
    cPrime = util.applyBitPermutation(util.pinv, util.xorBitList(rPrime, cons))

    e0 = util.applyBitPermutation(util.exp, lf0)
    e1 = util.applyBitPermutation(util.exp, lf1)
