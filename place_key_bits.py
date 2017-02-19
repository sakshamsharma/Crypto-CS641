mapping = [
    [24, 27, 21, 6, 11, 15],
    [13, 10, 25, 16, 3, 20],
    [5, 1, 22, 14, 8, 18],
    [26, 17, 9, 2, 23, 12],
    [51, 34, 41, 47, 29, 37],
    [40, 50, 33, 55, 43, 30],
    [54, 31, 49, 38, 44, 35],
    [56, 52, 32, 46, 39, 42],
    ]

counts = {
    1: 63,
    2: 10,
    5: 36,
    6: 52,
    7: 51,
    8: 15,
    }

key = [ 'X' for _ in range(56) ]

for (k, v) in counts.items():
  # k is sbox number, v is it's key value
  for i, bit in enumerate('{0:06b}'.format(v)):
    if bit == '1':
      key[mapping[k-1][i] - 1] = '1'
    else:
      key[mapping[k-1][i] - 1] = '0'

print(''.join(key))
