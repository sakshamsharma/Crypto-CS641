import requests as r
import multiprocessing.dummy
import string
import sys

if len(sys.argv) < 3:
  print('Expected input and output file')
  exit(0)

r.packages.urllib3.disable_warnings()

url = 'https://172.27.26.123:9999/des'
defbody = {'teamname': 'Gupt_Nashak', 'password': '3e5c2290d2dc86fe25d24eb6eb17fcf7'}

pool = multiprocessing.dummy.Pool(processes=100)

def getcipher(text):
  defbody['plaintext'] = text
  resp = r.post(url, json=defbody, verify=False)
  return resp.json()['ciphertext']

with open(sys.argv[1]) as f:
  text = f.readlines()

cnt = 0
f = open(sys.argv[2], 'w')

def getciphernetwork(plaintext):
  global cnt
  tosend = ''.join(plaintext.split(' ')).strip()
  sys.stdout.flush()
  cipher = getcipher(tosend)
  print(str(cnt) + ':' + tosend)
  f.write(tosend + ': ' + cipher + '\n')
  cnt = cnt + 1

pool.map(getciphernetwork, text)
f.close()
