import requests as r
import string
import sys

# NOT USEFUL APART FROM HELPING US DISCOVER
# THE INPUT OUTPUT MAPPING BY PROVIDING SOME DATA

r.packages.urllib3.disable_warnings()

# url = 'https://172.27.18.8:9999/des'
url = 'https://172.27.26.123:9999/des'
defbody = {'teamname': 'Gupt_Nashak', 'password': '3e5c2290d2dc86fe25d24eb6eb17fcf7'}

# Change this to get items in bulk
userinput = True
di = {  }

def getcipher(text):
  defbody['plaintext'] = text
  resp = r.post(url, json=defbody, verify=False)
  return resp.json()['ciphertext']

if userinput:
  while True:
    text = input()
    print(text + ': ' + getcipher(text))
    sys.stdout.flush()
else:
  # text = 'c'*1000
  # alphas = list(string.ascii_lowercase)
  # alphas.extend(list(string.ascii_uppercase))
  # alphas.extend(list(range(10)))
  text = [ (chr(x) + chr(y)) for x in range(33, 127) for y in range(33, 127)]

  with open('maps') as f:
    for plaintext in text:
      print(plaintext)
      cipher = getcipher(plaintext)
      f.write(plaintext + ': ' + cipher + '\n')
      di.setdefault(cipher, [])
      di[cipher].append(plaintext)

  for key in di:
    print(key + ': ')
    print(di[key])
