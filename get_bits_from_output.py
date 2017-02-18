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

with open(sys.argv[1]) as f:
  for line in f:
    line = line.rstrip().split(' ')
    line[0] = line[0].translate(trantab).replace(':', '')
    line[1] = line[1].translate(trantab).replace(':', '')
    in1, in2 = line[0][:len(line[0])//2], line[0][len(line[0])//2:]
    out1, out2 = line[1][:len(line[1])//2], line[1][len(line[1])//2:]

    # print(in1, in2, out1, out2)
    print(getbytestrings(in1))
