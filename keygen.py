import util
from get_some_key_bits import *
import itertools

partialkey = list('X01XX1XX00110X100XX01X11101X0011001X00110101X11X0110X110')
replaceLocations = [0, 3, 4, 6, 7, 13, 17, 18, 21, 27, 35, 44, 47, 52]

boom = [ ['0', '1'] for _ in range(14) ]
for replacement in itertools.product(*boom):
  kk = partialkey[:]
  for i in range(14):
    kk[replaceLocations[i]] = replacement[i]
  bitstring = ''.join(map(lambda x: str(x), kk))
  print(bitstring)
  # bitlist = toBitList(bitstring)
  # intlist = list(map(lambda x: bitListToInt(getblock(x, bitlist, 8)), range(1, 8)))
  # for i in intlist:
    # print(i, end=' ')
  # print()
